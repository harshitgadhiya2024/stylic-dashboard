from openai import OpenAI
from operations.mongo_operation import mongoOperation
from operations.prompt_generator import generate_fashion_prompt, single_generate_fashion_prompt
from utils.constant import constant_dict
import base64
import os, uuid

from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types

# Configuration parameters (same as your original)
model_generation_params = {
    "model_type": {
        "age_group": {
            "child": ["toddler", "young_child", "pre_teen"],
            "teen": ["early_teen", "mid_teen", "late_teen"],
            "adult": ["young_adult", "middle_aged", "mature_adult", "elderly"]
        },
        "gender": ["male", "female", "non_binary"],
        "ethnicity": ["caucasian", "african", "asian", "indian", "hispanic", "middle_eastern", "mixed", "other"]
    },
    "body_structure": {
        "height": ["very_short", "short", "average", "tall", "very_tall"],
        "build": {
            "weight": ["underweight", "slim", "average", "heavy", "obese"],
            "muscle_tone": ["skinny", "toned", "athletic", "muscular", "bodybuilder"],
            "body_shape": ["pear", "apple", "hourglass", "rectangle", "inverted_triangle"]
        }
    },
    "body_type": {
        "standing_pose": ["neutral", "confident", "sitting_casual", "action_pose", "relaxed"],
        "facial_expression": ["neutral", "smile", "serious", "joyful", "contemplative"],
        "hand_position": ["at_sides", "on_hips", "crossed", "gesturing", "in_pockets"]
    },
    "background": {
        "lighting": ["natural", "studio", "soft", "golden_hour"],
        "background": ["white", "neutral", "outdoor", "studio", "abstract", "contextual"],
        "camera_angle": ["eye_level", "slight_high", "slight_low", "close_up", "full_body"]
    },
    "body_pose": [
        "Full-View Front",
        "Close-Up Front",
        "Full-View Back",
        "Full-View Left Side Angle",
        "Full-View Right Side Angle",
        "Detail Shot (Front)",
        "Profile View Left",
        "Profile View Right",
        "Close-Up Back",
        "Close-Up Profile View",
        "Bottom Detailed Shot",
        "Bottom Close-Up Front",
        "Bottom Full-View Front",
        "Bottom Profile View",
        "Bottom Full-View Back",
        "Three-Quarter Front Left",
        "Three-Quarter Front Right",
        "Three-Quarter Back Left",
        "Three-Quarter Back Right",
        "Upper Body Profile Left",
        "Upper Body Profile Right",
        "Detail Shot (Back)",
        "Side Detail Shot",
        "Bottom Close-Up Back",
        "Bottom Three-Quarter View",
        "Full Body Side Angle",
        "Torso Detail Shot"
    ],
}

FACE_PARAMETERS = {
    "facial_structure": {
        "face_shape": ["oval", "round", "square", "heart-shaped", "diamond", "oblong"],
        "jawline": ["soft", "defined", "sharp", "angular"],
        "cheekbones": ["subtle", "moderate", "prominent", "high"]
    },
    "eyes": {
        "shape": ["almond", "round", "hooded", "deep-set", "upturned", "downturned"],
        "color": ["brown", "dark brown", "hazel", "green", "blue", "gray", "amber"],
        "size": ["small", "medium", "large"],
        "eyebrows": ["thin", "medium", "thick", "arched", "straight", "bushy"]
    },
    "nose": {
        "shape": ["straight", "button", "roman", "aquiline", "snub", "broad"],
        "size": ["small", "medium", "large"]
    },
    "mouth": {
        "lips": ["thin", "medium", "full", "very full"],
        "shape": ["straight", "bow-shaped", "wide", "small"]
    },
    "hair": {
        "color": ["black", "dark brown", "brown", "light brown", "blonde", "platinum", "red", "auburn", "gray",
                  "white"],
        "texture": ["straight", "wavy", "curly", "coily"],
        "length": ["very short", "short", "medium", "long", "very long"],
        "style": ["loose", "ponytail", "bun", "braided", "tousled", "sleek"]
    },
    "skin": {
        "tone": ["very fair", "fair", "light", "medium", "olive", "tan", "dark", "very dark"],
        "texture": ["smooth", "slightly textured", "freckled"]
    },
    "age": ["toddler", "young-child", "pre-teen", "early-teen", "mid-teen", "late-teen", "young-adult", "middle-aged",
            "mature-adult", "elderly"],
    "gender": ["male", "female", "non_binary"],
    "expression": ["neutral", "slight smile", "warm smile", "serious", "contemplative", "confident"],
    "lighting": ["soft natural light", "dramatic lighting", "golden hour", "studio lighting", "side lighting"]
}


class GarmentPhotoshootGenerator:
    def _init_(self):
        pass

    def validate_images(self, *image_paths):
        """Validate that all required images exist and are readable"""
        for path in image_paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Image not found: {path}")
            try:
                with Image.open(path) as img:
                    img.verify()
            except Exception as e:
                raise ValueError(f"Invalid image file {path}: {e}")

    def optimize_image_size(self, image_path, max_size=(1024, 1024)):
        """Resize image if it's too large for API"""
        with Image.open(image_path) as img:
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                optimized_path = f"optimized_{os.path.basename(image_path)}"
                img.save(optimized_path, quality=95)
                return optimized_path
        return image_path

    def generate_model_face(self, face_params, output_filename, photoshoot_id):
        """Generate a consistent model face based on parameters"""
        try:
            prompt = self.create_face_prompt(face_params)
            print(f"Generating face with prompt: {prompt}")
            client = OpenAI(
                api_key=constant_dict.get("openai_key"))

            result = client.images.generate(
                model="gpt-image-1",
                prompt=prompt
            )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            # Save the image to a file
            with open(f"static/photoshoots_folders/{photoshoot_id}/{output_filename}", "wb") as f:
                f.write(image_bytes)

            return output_filename

        except Exception as e:
            print(f"Error generating face: {e}")
            return None

    def create_face_prompt(self, params):
        """Create detailed face generation prompt"""
        try:
            prompt_parts = []

            # Basic description
            prompt_parts.append(
                f"{params['ethnicity']} Professional headshot portrait of a {params['age']} years of {params['gender']} person")

            # Hair
            hair_desc = f"{params['hair']['color']} hair color"
            prompt_parts.append(hair_desc)

            # Skin
            prompt_parts.append(f"{params['skin']['tone']} {params['skin']['texture']} skin")

            # Expression and lighting
            prompt_parts.append(f"{params['expression']} expression")
            prompt_parts.append(f"photographed with {params['lighting']}")

            # Quality descriptors
            prompt_parts.append("high resolution, photorealistic, professional photography, clean background")

            return ", ".join(prompt_parts)

        except Exception as e:
            print(f"Error creating face prompt: {e}")
            return ""

    def generate_photoshoot_image(self, photoshoot_id, image_prompt, face_image, garment_type, upper_garment,
                                  lower_garment, output_filename):
        """Generate photoshoot image with consistent face and garments"""
        try:
            upper_garment = f"static/photoshoots_folders/{photoshoot_id}/{upper_garment}"
            lower_garment = f"static/photoshoots_folders/{photoshoot_id}/{lower_garment}"
            face_image = f"static/photoshoots_folders/{photoshoot_id}/{face_image}"

            client = OpenAI(
                api_key=constant_dict.get("openai_key"))

            if garment_type == "upper_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(face_image, "rb"), open(upper_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            elif garment_type == "lower_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(face_image, "rb"), open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            elif garment_type == "full_body_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(face_image, "rb"), open(upper_garment, "rb"), open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            elif garment_type == "one_piece_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(face_image, "rb"), open(upper_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )
            elif garment_type == "full_body_dress_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(face_image, "rb"), open(upper_garment, "rb"), open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )
            else:
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(face_image, "rb"), open(upper_garment, "rb"), open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            with open(f"static/photoshoots_folders/{photoshoot_id}/{output_filename}", "wb") as f:
                f.write(image_bytes)
            return "done"

        except Exception as e:
            print(f"Error generating photoshoot image: {e}")
            return None

    def single_generate_photoshoot_image(self, photoshoot_id, image_prompt, face_image, garment_type, upper_garment,
                                  lower_garment, output_filename):
        """Generate photoshoot image with consistent face and garments"""
        try:
            if upper_garment:
                upper_garment = f"static/photoshoots_folders/{photoshoot_id}/{upper_garment}"
            lower_garment = f"static/photoshoots_folders/{photoshoot_id}/{lower_garment}"

            client = OpenAI(
                api_key=constant_dict.get("openai_key"))

            if garment_type == "upper_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(upper_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            elif garment_type == "lower_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            elif garment_type == "full_body_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(upper_garment, "rb"), open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            elif garment_type == "one_piece_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(upper_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )
            elif garment_type == "full_body_dress_garment":
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(upper_garment, "rb"), open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )
            else:
                result = client.images.edit(
                    model="gpt-image-1",
                    image=[open(upper_garment, "rb"), open(lower_garment, "rb")],
                    prompt=image_prompt,
                    input_fidelity="high"
                )

            image_base64 = result.data[0].b64_json
            image_bytes = base64.b64decode(image_base64)

            with open(f"static/photoshoots_folders/{photoshoot_id}/{output_filename}", "wb") as f:
                f.write(image_bytes)
            return "done"

        except Exception as e:
            print(f"Error generating photoshoot image: {e}")
            return None


def generate_photoshoot_background_task(garment_mapping_dict, photoshoot_id, upper_garment_filename,
                                        lower_garment_filename, lower_garment_type, upper_garment_type, lower_garment_specs, upper_garment_specs, garment_type):
    """
    Background task for generating photoshoot images
    """
    try:
        # Update status to processing
        user_id = garment_mapping_dict.get("id")

        mongoOperation().update_mongo_data(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id},
            {"status": "processing"}
        )

        gender = garment_mapping_dict.get("gender")
        ethnicity = garment_mapping_dict.get("ethnicity")
        fitting = garment_mapping_dict.get("fitting")
        age = garment_mapping_dict.get("age")

        poses = garment_mapping_dict.get("selected_poses", [])

        all_generated_images = []

        mongoOperation().update_mongo_data(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id},
            {"status": "process started"}
        )


        upper_garment_image = upper_garment_filename
        below_garment_image = lower_garment_filename

        fashion_poses = [
            "Model standing straight, facing camera, hands on hips, confident look, full outfit in view",
            "Model in relaxed stance, one leg slightly forward, arms crossed, looking to side",
            "Model standing with one arm raised, leaning slightly back, dramatic lighting",
            "Model walking forward, mid-stride, natural motion, wind in hair or fabric",
            "Model standing sideways, looking over shoulder, showing side profile and outfit shape",
            "Model leaning slightly on wall, hands in pockets, casual expression",
            "Model with arms crossed behind back, clean backdrop, neutral lighting",
            "Model holding a handbag with one hand, other hand on waist, urban background",
            "Model adjusting sunglasses or collar, slightly looking down, fashion-forward angle",
            "Model standing on one leg with the other bent, playful posture, vibrant mood",
            "Model sitting on stool, one leg crossed over the other, hands on lap, straight back",
            "Model leaning forward on knees, elbows on thighs, intense eye contact",
            "Model lounging on couch, legs extended, arm behind head, relaxed elegance",
            "Model sitting sideways on stairs, chin resting on hand, urban style",
            "Model sitting cross-legged on floor, looking up slightly, natural pose",
            "Model seated on high chair, legs crossed, arms resting casually, studio backdrop",
            "Model with one knee up, seated on step, elbows resting on knee, thoughtful look",
            "Model reclining slightly on floor with one arm supporting upper body, full outfit visible",
            "Model sitting on window ledge, sunlight hitting face, casual urban vibe",
            "Model sitting backwards on chair, arms resting on backrest, bold streetwear pose",
            "Model in high-fashion stance, one foot forward, hips tilted, dramatic pose with shadows",
            "Model holding flowing fabric in motion, elegant long dress, wind effect",
            "Model in asymmetrical pose, arm lifted, intense makeup and styling",
            "Model in power pose, hands on waist, wide-legged stance, blazer and heels",
            "Model leaning dramatically to side, high contrast lighting, editorial look",
            "Model crouching low with head turned toward camera, street style outfit",
            "Model posing with garment in motion, twirling or flipping skirt, studio setup",
            "Model with arms spread out, coat open wide, walking with confidence",
            "Model using accessory as a prop (hat, handbag), interacting naturally with it",
            'Lower half shot - Model standing with legs shoulder-width apart, showcasing trouser fit and length against studio grey backdrop',
            "Hip down view - Model with one leg stepped forward, highlighting jeans' design and pocket details with urban street background",
            "Waist to feet - Model in walking stride, showing skirt's movement and flow against minimalist white studio setup",
            "Lower body - Model with weight on one leg, displaying pants' side seam and fit with natural outdoor lighting",
            "Legs focus - Model sitting on stool with legs crossed, featuring dress pants' crease and fabric against wooden backdrop",
            "Hip level down - Model leaning against wall, showing shorts' length and style with brick wall industrial background",
            'Lower torso - Model with hands in pockets, highlighting trouser waistband and belt details against concrete texture wall',
            "Leg shot - Model in lunging position, showcasing leggings' stretch and fit with modern gym/studio lighting",
            "Waist down - Model standing on stairs, displaying skirt's layered design and hemline with urban architectural background",
            "Lower body angle - Model with one foot on elevated surface, showing boot-cut jeans' silhouette against rustic wooden fence",
            'Upper half shot - Model standing straight with hands on hips, showcasing blouse details against white studio backdrop',
            'Torso view - Model with arms crossed, highlighting blazer texture and fit with soft grey gradient background',
            'Chest up shot - Model adjusting collar with one hand, emphasizing shirt design against minimalist concrete wall',
            "Upper body - Model with one arm raised above head, showing top's drape and movement with natural window lighting",
            'Waist up - Model leaning slightly forward, hands clasped behind back, featuring sweater details on rustic brick background',
            'Bust level shot - Model with arms extended sideways, displaying jacket sleeves and shoulder line against black studio backdrop',
            'Upper torso - Model holding lapels of coat, showing upper garment structure with moody dark lighting setup',
            "Chest focus - Model with one hand on shoulder, other on waist, highlighting top's neckline against marble texture background",
            'Shoulder up - Model adjusting cufflinks or sleeves, emphasizing shirt details with warm golden hour lighting',
            "Upper body angle - Model with arms crossed at chest level, showcasing cardigan's button details against vintage wooden backdrop",
            'Saree drape display - Model standing with pallu arranged, showcasing traditional drape and pleats against ornate palace background',
            "Evening dress elegance - Model in formal stance, highlighting gown's silhouette and train with luxury hotel ballroom setting",
            "Saree pallu flow - Model with pallu in motion, showing fabric's movement and border details with traditional courtyard backdrop",
            'Cocktail dress pose - Model adjusting dress strap, emphasizing neckline and fit with upscale rooftop city view background',
            "Traditional saree sit - Model sitting gracefully, displaying saree's fall and blouse design with carved stone architecture setting",
            "Formal dress stance - Model with hands clasped, showcasing dress's structure and length with modern corporate lobby background",
            "Saree walking pose - Model in motion, showing saree's grace and pleated movement with heritage building corridor backdrop",
            "Party dress twirl - Model spinning, displaying dress's flare and fabric flow with glamorous nightclub lighting setup",
            'Saree blouse focus - Model adjusting jewelry, highlighting blouse design and saree coordination with traditional Indian interior',
            'Maxi dress breeze - Model outdoors with dress flowing, showcasing length and movement with scenic landscape background',
            'Full dress display - Model standing straight with arms at sides, showcasing dress silhouette and length against white studio backdrop',
            'Jumpsuit stance - Model with one hand on hip, other adjusting strap, highlighting one-piece design with modern architectural background',
            "Romper pose - Model in playful stance with legs apart, showing garment's shorts and top integration against colorful graffiti wall",
            'Maxi dress flow - Model walking with fabric in motion, displaying dress length and movement with natural outdoor garden setting',
            'Overall showcase - Model with hands in pockets, casual stance highlighting denim one-piece against rustic barn background',
            "Bodysuit emphasis - Model in stretching pose, showing garment's fitted silhouette and flexibility with contemporary dance studio lighting",
            "Midi dress twirl - Model spinning with dress flowing, capturing garment's movement and shape against seamless grey backdrop",
            'Catsuit display - Model in power pose with wide stance, showcasing fitted one-piece design with dramatic studio lighting',
            "Wrap dress pose - Model adjusting wrap tie, showing dress's unique closure and drape with soft natural window lighting",
            'Palazzo jumpsuit - Model with arms extended, displaying wide-leg one-piece silhouette against minimalist concrete wall background',
            'Full body - Model standing straight facing camera with hands on hips, confident look showcasing complete outfit against white studio backdrop',
            'Complete view - Model in relaxed stance with one leg slightly forward, arms crossed, looking to side against grey gradient background',
            'Full figure - Model standing with one arm raised, leaning slightly back with dramatic lighting on textured concrete wall',
            'Whole body - Model walking forward mid-stride, natural motion with wind effect against urban street background',
            'Full length - Model standing sideways looking over shoulder, showing side profile and outfit shape with natural window lighting',
            'Complete shot - Model leaning slightly on wall with hands in pockets, casual expression against brick texture backdrop',
            'Full body angle - Model with arms crossed behind back, clean full outfit display with minimalist studio lighting',
            'Entire figure - Model holding handbag with one hand, other on waist against modern city skyline background',
            'Full view - Model adjusting sunglasses while looking down, fashion-forward angle with golden hour outdoor lighting',
            'Complete pose - Model standing on one leg with other bent, playful posture showing full outfit against vibrant colored backdrop'
        ]
        main_poses = [
            # Front Standing Poses
            "half-upper-body Model standing straight facing camera, arms relaxed at sides, shoulders back, chin slightly raised, direct eye contact, showcasing front design and fit of upper garment",

            "half-upper-body Model in three-quarter stance, one hand on hip, other arm hanging naturally, weight shifted to one leg, highlighting garment's silhouette and drape",

            "half-upper-body Model standing with arms crossed casually over chest, confident expression, shoulders slightly forward, emphasizing garment's chest area and sleeve details",

            "half-upper-body Model with hands clasped behind back, chest open, standing tall with perfect posture, displaying front panel and neckline of garment clearly",

            "half-upper-body Model reaching one arm across body to opposite shoulder, other arm relaxed, creating diagonal lines that showcase garment's stretch and fit",

            # Back Standing Poses
            "half-upper-body Model standing with back to camera, looking over shoulder, arms at sides, showcasing back design, seams, and overall rear silhouette of garment",

            "half-upper-body Model facing away from camera, arms crossed behind back, head turned slightly to show profile, highlighting back construction and shoulder details",

            "half-upper-body Model with back to camera, one hand running through hair, other arm extended slightly, displaying back drape and how garment falls naturally",

            "half-upper-body Model standing with back facing camera, both arms raised touching back of neck/head, showing garment's back design and armhole construction",

            "half-upper-body Model in back view, leaning against wall with one shoulder, arms relaxed, demonstrating garment's back fit and movement",

            # Side Profile Poses
            "half-upper-body Model in perfect side profile, chin raised, arms positioned naturally at sides, showcasing garment's side seams and overall side silhouette",

            "half-upper-body Model in side stance with arms crossed, looking straight ahead, displaying side design elements and how garment fits across torso",

            "half-upper-body Model in three-quarter back view, slight turn toward camera, one hand on hip, showing garment's back and side construction details",

            # Sitting Poses - Front Focus
            "half-upper-body Model sitting forward on edge of seat, elbows resting on knees, leaning toward camera, highlighting how garment drapes when seated",

            "half-upper-body Model sitting relaxed with one arm draped over chair back, other hand on leg, showcasing garment's comfort and movement in seated position",

            "full-body Model sitting cross-legged, hands resting on ankles, straight posture, displaying garment's fit and comfort in relaxed sitting pose",

            # Sitting Poses - Back Focus
            "half-upper-body Model sitting facing away from camera on chair, looking back over shoulder, arms resting naturally, showing garment's back design in seated position",

            "half-upper-body Model sitting sideways on chair, both arms on chair back, looking toward camera, displaying side and partial back view of garment",

            # Dynamic Movement Poses
            "full-body Model captured mid-stride walking toward camera, arms naturally swinging, showcasing how garment moves and flows with body motion",

            "full-body Model in turning motion, arms slightly outstretched, fabric catching movement, displaying garment's flexibility and drape during motion",

            "full-body Model stepping forward with one foot, arms positioned in natural walking gesture, highlighting garment's comfort during movement",

            # Arm Positioning - Front Focus
            "half-upper-body Model with both hands running through hair, elbows raised, eyes looking up, showcasing garment's armhole construction and chest area",

            "half-upper-body Model with one hand touching neck/collar area gently, other arm relaxed at side, highlighting neckline and upper garment details",

            "half-upper-body Model with arms stretched overhead, displaying garment's length, side seams, and how it maintains shape when arms are raised",

            "half-upper-body Model adjusting sleeves or cuffs with focused downward gaze, showcasing garment's sleeve details and construction",

            # Arm Positioning - Back Focus
            "half-upper-body Model facing away with both arms raised above head, showing garment's back design and how it responds to arm movement",

            "half-upper-body Model with back to camera, one hand touching opposite shoulder blade, other arm relaxed, displaying back construction and fit",

            "half-upper-body Model facing away, arms positioned as if stretching or reaching, showcasing back panel design and shoulder construction",

            # Leaning and Support Poses
            "half-upper-body Model leaning against wall with one shoulder, arms crossed, relaxed expression, showing how garment drapes against body and surface",

            "half-upper-body Model leaning back against surface with arms at sides, displaying garment's front design and natural drape",

            "half-upper-body Model leaning forward slightly, hands on hips, showcasing garment's fit and how it maintains shape when body leans",

            # Interactive Lifestyle Poses
            "half-upper-body Model reaching up toward something above, showing garment's movement, stretch, and how it maintains coverage during reaching motion",

            "half-upper-body Model positioned as if adjusting or examining garment details, hands naturally interacting with fabric, showcasing construction and fit",

            "half-upper-body Model in casual pose suggesting everyday wear, arms positioned naturally for daily activities, highlighting garment's practicality and comfort",

            # Close-up Upper Body Focus
            "half-upper-body Model upper body shot with arms positioned to frame torso, emphasizing garment's neckline, shoulder construction, and upper chest area",

            "half-upper-body Model with one arm across body, hand resting on opposite arm, creating interesting lines while showcasing sleeve and body construction",

            "half-upper-body Model with hands clasped in front, arms creating frame for garment's center panel and front design elements",

            # Back Detail Poses
            "half-upper-body Model with back three-quarters to camera, one arm reaching across to opposite shoulder, showing back construction and shoulder mobility",

            "half-upper-body Model facing completely away, arms hanging naturally, perfect back view showcasing rear design, seam placement, and overall back silhouette",

            "half-upper-body Model with back to camera, hands on hips, elbows out, displaying back width, construction details, and how garment fits across shoulder blades",

            # Front Standing Poses - Full Body
            "full-body Full body shot of model standing straight facing camera, arms relaxed at sides, feet shoulder-width apart, showcasing complete garment silhouette and proportions",

            "full-body Model in confident full body stance, one hand on hip, other arm hanging naturally, weight shifted to one leg, displaying garment's overall fit and drape",

            "full-body Full body pose with model standing, arms crossed casually over chest, legs positioned naturally, emphasizing garment's relationship to lower body proportions",

            "full-body Model standing with hands clasped behind back, full body visible, chest open and shoulders back, showing garment's front design in complete context",

            "full-body Full body shot with model reaching one arm across body to opposite shoulder, creating diagonal lines, showcasing garment's stretch and complete silhouette",

            # Back Standing Poses - Full Body
            "full-body Complete back view of model standing with back to camera, looking over shoulder, full body visible, showcasing garment's back design and overall rear silhouette",

            "full-body Full body back pose with model facing away, arms crossed behind back, legs positioned naturally, highlighting garment's back construction and proportions",

            "full-body Model with back to camera, full body shot, one hand running through hair, other arm extended, displaying complete back view and garment movement",

            "full-body Full body back view with model standing, both arms raised touching back of neck, showing garment's back design and how it interacts with body lines",

            "full-body Complete back pose of model leaning against wall with one shoulder, full body visible, demonstrating garment's back fit and natural drape",

            # Side Profile Poses - Full Body
            "full-body Full body side profile of model with chin raised, arms positioned naturally, showcasing complete side silhouette and garment's side construction",

            "full-body Complete side view with model in confident stance, arms crossed, displaying full side design elements and garment's interaction with body profile",

            "full-body Full body three-quarter back view, slight turn toward camera, one hand on hip, showing garment's back and side construction in complete context",

            # Chair and Furniture Poses
            "full-body Model sitting on modern chair, leaning back with one leg crossed over the other, arms draped naturally on armrests, showcasing garment's seated fit and drape",

            "full-body Model perched on edge of desk or table, legs dangling, hands gripping edge for support, displaying garment's movement and fit in elevated sitting position",

            "full-body Model sitting backwards on chair, straddling seat, arms resting on chair back, facing camera, highlighting garment's front design in unique seating pose",

            "full-body Model lounging in oversized armchair, one leg tucked under, other foot on floor, arm draped over chair arm, showing garment's comfort and relaxed fit",

            "full-body Model sitting on bar stool or high chair, feet resting on footrest, hands on knees, showcasing garment's proportions on elevated seating",

            "full-body Model sitting sideways on bench, one leg up on bench, other foot on ground, hands positioned naturally, displaying garment's flexibility and fit",

            # Sunglasses Poses
            "half-upper-body Model wearing sunglasses, standing confidently with hands on hips, showcasing garment while sunglasses add stylish accessory element to overall look",

            "half-upper-body Model with sunglasses pushed up on head, one hand adjusting them, other arm relaxed, highlighting garment while interacting with eyewear accessory",

            "half-upper-body Model wearing sunglasses, arms crossed casually, leaning against wall, displaying garment's style coordination with fashionable sunglasses accessory",

            "half-upper-body Model holding sunglasses in one hand, other hand on hip, showcasing garment while suggesting transition from indoor to outdoor styling",

            "half-upper-body Model putting on or taking off sunglasses, arms raised to face, displaying garment's fit and movement during natural accessory interaction",

            # Bag and Purse Poses
            "half-upper-body Model holding small handbag or clutch in one hand, other arm relaxed at side, showcasing how garment coordinates with carried accessories",

            "half-upper-body Model with crossbody bag or purse strap across chest, hands positioned naturally, displaying garment's interaction with bag accessories",

            "half-upper-body Model adjusting or looking through handbag contents, showcasing garment during natural everyday accessory interaction and usage",

            "half-upper-body Model holding tote bag or larger purse with both hands, arms extended slightly, displaying garment's proportions with larger accessory pieces",

            "half-upper-body Model with bag slung over shoulder, one hand holding strap, other hand free, showcasing garment's coordination with shoulder-carried accessories",

            # Lighting and Lamp Props
            "half-upper-body Model holding ring light or small lighting prop, arms extended, showcasing garment while interacting with photography or beauty equipment",

            "half-upper-body Model positioned near desk lamp or floor lamp, one hand touching or adjusting light, displaying garment in workspace or home environment setting",

            "half-upper-body Model holding string lights or fairy lights, arms arranged to display lights, showcasing garment while creating atmospheric lighting prop interaction",

            "half-upper-body Model with hands cupped around small light source or candle, face illuminated, displaying garment in intimate lighting prop scenario",

            # Book and Reading Props
            "full-body Model sitting with open book in lap, one hand holding pages, other arm resting naturally, showcasing garment during reading or studying pose",

            "half-upper-body Model standing while reading book, holding it with both hands, displaying garment during intellectual or leisure activity with literary prop",

            "half-upper-body Model holding stack of books against chest with one arm, other hand free, showcasing garment while carrying educational or work-related props",

            "full-body Model sitting cross-legged on floor with book open, leaning over to read, displaying garment's comfort and flexibility during reading activity",

            # Coffee and Beverage Props
            "half-upper-body Model holding coffee cup or mug with both hands near chest, steam visible, showcasing garment during cozy morning or café moment with beverage prop",

            "half-upper-body Model sitting at table with coffee cup, one hand on cup handle, other arm resting on table, displaying garment in café or breakfast setting",

            "half-upper-body Model holding water bottle or drink, about to take sip, showcasing garment during hydration or fitness-related prop interaction",

            "half-upper-body Model raising coffee cup in toast gesture, other hand on hip, displaying garment during celebratory or social beverage moment",

            # Phone and Technology Props
            "half-upper-body Model holding smartphone, looking at screen or taking selfie, showcasing garment during modern technology interaction and daily phone usage",

            "half-upper-body Model talking on phone, one hand holding device to ear, other arm gesturing naturally, displaying garment during communication activity",

            "half-upper-body Model sitting with laptop on lap, hands on keyboard, showcasing garment during work or study activity with technology props",

            "half-upper-body Model holding tablet or e-reader, looking at screen, displaying garment during digital reading or entertainment activity",

            # Flower and Plant Props
            "half-upper-body Model holding bouquet of flowers with both hands, flowers positioned near chest area, showcasing garment while interacting with natural floral props",

            "half-upper-body Model smelling single flower, holding it delicately near face, other arm relaxed, displaying garment during romantic or natural moment with flower prop",

            "half-upper-body Model sitting near or tending to potted plant, hands interacting with leaves or pot, showcasing garment during gardening or plant care activity",

            "half-upper-body Model holding small succulent or plant pot, arms positioned to display both plant and garment effectively in nature-inspired prop scenario",

            # Music and Instrument Props
            "half-upper-body Model holding acoustic guitar, hands positioned on strings and neck, showcasing garment while interacting with musical instrument prop",

            "half-upper-body Model with headphones around neck or on head, hands adjusting them, displaying garment while engaging with music-related accessory props",

            "half-upper-body Model holding vinyl record or CD, examining it or about to play it, showcasing garment during music appreciation or entertainment activity",

            # Art and Creative Props
            "half-upper-body Model holding paintbrush or art supplies, hands positioned as if creating, showcasing garment during artistic or creative activity with art props",

            "half-upper-body Model sitting at easel or art station, hands working with creative materials, displaying garment during artistic pursuit or hobby activity",

            "half-upper-body Model holding camera, positioned as if taking photos, showcasing garment while engaging with photography equipment and creative props",

            "half-upper-body Model with art palette or sketchbook, hands positioned for creative work, displaying garment during artistic expression or learning activity",

            # Mirror and Reflection Props
            "half-upper-body Model looking in handheld mirror, one hand holding mirror, other touching face or hair, showcasing garment during grooming or beauty routine",

            "full-body Model positioned near full-length mirror, looking at reflection, showcasing garment while checking appearance or getting ready",

            "half-upper-body Model holding compact mirror, checking reflection, other hand free, displaying garment during quick beauty check or touch-up moment",

            # Food and Kitchen Props
            "half-upper-body Model holding piece of fruit or small snack, positioned near mouth as if eating, showcasing garment during casual dining or healthy eating moment",

            "half-upper-body Model sitting at kitchen counter with breakfast items, hands interacting with food props, displaying garment in morning routine or meal setting",

            "half-upper-body Model holding cooking utensil or kitchen tool, positioned as if preparing food, showcasing garment during culinary or domestic activity",

            # One-Piece Garment Specific Poses - Standing
            "full-body Model standing with arms raised above head in celebration pose, showcasing one-piece garment's full length and complete silhouette from neckline to hemline",

            "full-body Model in asymmetrical standing pose, one hip jutted out, arms positioned at different heights, displaying one-piece garment's fit across entire torso and body",

            "full-body Model standing with one leg stepped forward, hands on waist, highlighting one-piece garment's proportions and how it flatters the complete figure",

            "full-body Model in twisting motion, body turned at waist, arms following the movement, showcasing one-piece garment's flexibility and drape during body rotation",

            "full-body Model standing with arms stretched wide, displaying one-piece garment's width, armhole construction, and overall coverage from shoulders to bottom hem",

            # One-Piece Garment Specific Poses - Sitting
            "full-body Model sitting on floor with legs extended straight, leaning back on hands, showcasing how one-piece garment maintains coverage and style in floor sitting position",

            "full-body Model sitting cross-legged with perfect posture, hands resting on ankles, displaying one-piece garment's comfort and drape in relaxed ground sitting pose",

            "full-body Model sitting on chair with legs tucked to one side, showcasing one-piece garment's elegance and how it flows when legs are positioned asymmetrically",

            "full-body Model sitting sideways on chair or stool, one leg hanging down, other tucked up, displaying one-piece garment's adaptability to various sitting positions",

            "full-body Model perched on chair arm or elevated surface, both legs dangling, showcasing one-piece garment's coverage and style in elevated casual seating",

            # One-Piece Garment Specific Poses - Movement
            "full-body Model captured mid-spin with arms outstretched, showcasing one-piece garment's movement, flow, and how fabric responds to rotational body motion",

            "full-body Model in walking motion with exaggerated step, displaying one-piece garment's movement and drape during natural locomotion and stride",

            "full-body Model jumping or leaping with arms and legs positioned dynamically, showcasing one-piece garment's flexibility and coverage during energetic movement",

            "full-body Model in dance-inspired pose with fluid arm and leg positioning, displaying one-piece garment's grace and movement during expressive body positions",

            "full-body Model stepping up onto platform or step, one leg raised, showcasing one-piece garment's functionality and style during elevation changes",

            # One-Piece Garment Specific Poses - Stretching
            "full-body Model reaching upward with both arms, body extended vertically, showcasing one-piece garment's length and how it maintains coverage during vertical stretch",

            "full-body Model in side stretch pose, one arm reaching over head to opposite side, displaying one-piece garment's flexibility and fit during lateral body movement",

            "full-body Model bending forward slightly with arms hanging naturally, showcasing one-piece garment's drape and coverage when body is angled downward",

            "half-upper-body Model in back arch pose with hands on lower back, chest open, displaying one-piece garment's fit and stretch across chest and torso areas",

            # One-Piece Garment Specific Poses - Lying Down
            "full-body Model lying on side with legs stacked, head propped on hand, showcasing one-piece garment's drape and fit in relaxed horizontal position",

            "full-body Model lying on back with arms stretched overhead, displaying one-piece garment's complete length and how it maintains shape when body is horizontal",

            "full-body Model in casual reclined position against pillows or cushions, showcasing one-piece garment's comfort and style in relaxed lounging pose",

            # One-Piece Garment Specific Poses - Hands on Garment
            "full-body Model smoothing or adjusting one-piece garment at waist area, showcasing fit and how hands naturally interact with the garment's silhouette",

            "full-body Model holding or lifting hem of one-piece garment slightly, displaying length and hemline details while showing garment's complete coverage",

            "half-upper-body Model adjusting neckline or shoulder area of one-piece garment, showcasing upper construction and fit across chest and shoulder areas",

            "full-body Model with hands positioned to show off specific details of one-piece garment, such as pockets, seams, or design elements along the silhouette",

            # Traditional Draped Garment Poses - Standing
            "full-body Model standing in classic pose with draped fabric arranged elegantly over one shoulder, other arm gracefully positioned at waist, showcasing traditional draping and flow",

            "full-body Model in regal standing position with draped fabric flowing behind, one hand holding fabric edge delicately, displaying traditional garment's grandeur and movement",

            "full-body Model standing with draped fabric wrapped around torso, arms positioned to show fabric's natural fall and traditional construction methods",

            "full-body Model in confident stance with draped garment's pleats arranged perfectly, one hand adjusting drape at shoulder, showcasing traditional styling techniques",

            "full-body Model standing with draped fabric creating elegant silhouette, both arms positioned to display how traditional garment frames the body naturally",

            # Traditional Draped Garment Poses - Movement
            "full-body Model captured mid-twirl with draped fabric spinning outward, creating circular motion that displays fabric's flow and traditional garment's dynamic beauty",

            "full-body Model in walking pose with draped fabric flowing behind in graceful movement, showcasing traditional garment's elegance during natural motion",

            "full-body Model stepping gracefully with one foot forward, draped fabric arranged in elegant folds, displaying traditional garment's grace during movement",

            "full-body Model in dance-inspired pose with draped fabric creating beautiful lines, arms positioned to enhance traditional garment's artistic draping",

            "full-body Model turning with draped fabric following body movement, showcasing traditional garment's fluid response to body rotation and motion",

            # Traditional Fitted Top and Flared Bottom Combination Poses
            "full-body Model standing with arms raised to show fitted upper portion construction, flared lower section displayed in full circular spread around legs",

            "full-body Model in spinning motion with fitted top maintaining shape while flared bottom creates dramatic circle, showcasing contrast between fitted and flowing elements",

            "full-body Model sitting on floor with fitted portion displayed clearly, flared bottom arranged in elegant circle around seated position",

            "full-body Model in dancing pose with fitted top showing construction details, flared bottom capturing motion and traditional garment's dynamic movement",

            "full-body Model standing on elevated surface with fitted upper portion visible, flared bottom cascading down to showcase traditional garment's dramatic silhouette",

            # Traditional Ethnic Ensemble Poses - Three-Piece Coordination
            "full-body Model standing with arms positioned to display all three coordinated pieces working together, showcasing traditional ensemble's harmony and proportion",

            "full-body Model in twirling motion showing how all three pieces move together in unified flow, displaying coordinated traditional garment set's collective beauty",

            "full-body Model sitting gracefully with three-piece ensemble arranged to show each component's role in overall traditional look and styling",

            "full-body Model in profile pose displaying three-piece traditional ensemble's silhouette and how each component contributes to complete traditional appearance",

            "full-body Model standing with hands positioned to adjust or display different elements of three-piece traditional ensemble, showing garment interaction and styling",

            # Traditional Formal Dress Poses - Full Length
            "full-body Model standing regally in full-length traditional formal garment, arms positioned gracefully, showcasing garment's complete formal silhouette and elegance",

            "full-body Model walking in full-length formal traditional garment, fabric flowing naturally, displaying how formal traditional wear moves with dignified grace",

            "full-body Model seated formally with full-length traditional garment arranged elegantly around chair, showcasing formal traditional wear's seated presentation",

            "full-body Model in formal traditional pose with full-length garment displayed completely, arms and posture reflecting traditional formal wearing customs and etiquette",

            "full-body Model standing with full-length traditional formal wear, one hand lifting fabric edge slightly to show garment details and traditional craftsmanship",

            # Traditional Garment Detail Poses
            "half-upper-body Model adjusting traditional garment's draping or pleating, hands delicately positioned to show proper traditional wearing technique and styling method",

            "half-upper-body Model displaying traditional garment's decorative elements by positioning arms and body to highlight embellishment areas and traditional design features",

            "full-body Model showing traditional garment's layering technique, hands positioned to demonstrate how different pieces work together in traditional ensemble coordination",

            "full-body Model in pose that displays traditional garment's construction details, body positioned to show seaming, gathering, or traditional tailoring methods",

            "full-body Model demonstrating traditional garment's versatility by adjusting draping or styling, showing different ways traditional wear can be arranged and presented",

            # Traditional Garment Sitting Poses
            "full-body Model sitting cross-legged on floor with traditional garment arranged in elegant circle, showcasing how traditional wear adapts to ground sitting",

            "full-body Model sitting on traditional low seating with garment flowing naturally, displaying traditional wear's compatibility with cultural seating customs",

            "full-body Model sitting sideways with traditional garment draped elegantly, showing how traditional wear maintains grace in various sitting positions",

            "full-body Model sitting with traditional garment's layers arranged carefully, displaying how multiple traditional pieces coordinate when seated",

            "full-body Model in formal sitting pose with traditional garment presented properly, showing traditional etiquette and proper wearing customs for formal occasions",

            # Additional Ethnic Wear Poses - Regional Variations
            "full-body Model standing with ethnic garment's regional styling elements highlighted, arms positioned to show unique cultural construction details and traditional craftsmanship techniques",

            "full-body Model in traditional cultural greeting pose with ethnic wear displayed properly, showcasing how garment coordinates with cultural customs and traditional gestures",

            "full-body Model walking with ethnic garment flowing in traditional manner, displaying regional wearing style and how garment moves according to cultural movement patterns",

            "full-body Model seated in traditional cultural posture with ethnic wear arranged according to regional customs, showcasing proper traditional sitting style and garment presentation",

            "full-body Model demonstrating traditional cultural dance movement with ethnic garment, displaying how traditional wear enhances cultural artistic expression and performance",

            # Ethnic Wear with Traditional Accessories Integration
            "full-body Model adjusting traditional head covering or veil with ethnic garment, hands positioned to show how traditional accessories complement the overall cultural ensemble",

            "full-body Model wearing traditional footwear with ethnic garment, standing pose that displays complete traditional outfit coordination from head to toe",

            "half-upper-body Model with traditional jewelry positioned to complement ethnic wear, arms arranged to show how accessories enhance traditional garment's cultural authenticity",

            "full-body Model holding traditional cultural prop or ceremonial item with ethnic garment, displaying how traditional wear coordinates with cultural objects and customs",

            "full-body Model in pose showing traditional waist accessories or belt with ethnic wear, hands positioned to highlight how traditional accessories complete the cultural look",

            # Ethnic Wear Ceremonial and Festival Poses
            "full-body Model in celebratory pose with ethnic garment arranged for festival or ceremony, arms raised in traditional celebration gesture showcasing festive wear styling",

            "full-body Model kneeling in traditional ceremonial position with ethnic garment flowing properly, displaying how traditional wear maintains dignity in cultural ceremonies",

            "full-body Model in traditional prayer or meditation pose with ethnic garment arranged respectfully, showcasing how traditional wear supports spiritual and cultural practices",

            "half-upper-body Model performing traditional offering gesture with ethnic garment, hands positioned in cultural greeting or blessing pose with traditional wear displayed properly",

            "full-body Model in traditional wedding or celebration pose with elaborate ethnic garment, showcasing how formal traditional wear is presented during important cultural ceremonies",

            # Ethnic Wear Layering and Draping Techniques
            "full-body Model demonstrating traditional layering technique with multiple ethnic garment pieces, showing how different traditional layers work together in cultural dressing",

            "full-body Model adjusting traditional wrap or shawl with ethnic ensemble, displaying proper traditional draping technique and cultural wearing methods",

            "full-body Model showing seasonal ethnic wear adaptation, with traditional layering or draping adjusted for cultural climate considerations and seasonal traditional practices",

            "full-body Model in pose displaying ethnic garment's modular construction, showing how traditional pieces can be arranged differently for various cultural occasions",

            "full-body Model demonstrating traditional gender-specific wearing style with ethnic garment, showcasing cultural dressing customs and traditional gender presentation in clothing",

            # Ethnic Wear Intergenerational and Cultural Continuity Poses
            "full-body Model in pose reflecting traditional cultural values with ethnic wear, posture and hand positioning showing respect for cultural heritage and traditional customs",

            "full-body Model displaying ethnic garment with traditional age-appropriate styling, showing how traditional wear adapts across different life stages while maintaining cultural authenticity",

            "full-body Model in educational pose with ethnic garment, positioned to teach traditional wearing techniques and cultural significance of traditional clothing elements",

            "full-body Model showing ethnic garment's everyday versus ceremonial presentation, demonstrating versatility of traditional wear in different cultural contexts and occasions",

            "full-body Model in pose that bridges traditional and contemporary styling with ethnic wear, showing how traditional garments maintain cultural relevance in modern contexts",

            # Draped Garment Standing Poses - Lower Body Focus
            "full-body Model standing with draped garment flowing around legs, one foot slightly forward, showcasing lower body draping technique and how fabric falls naturally around the legs",

            "full-body Model in confident stance with draped fabric arranged around hips and thighs, hands adjusting lower drape, displaying traditional lower body wrapping and styling methods",

            "full-body Model standing with draped garment's lower portion spread elegantly, legs positioned to show fabric's flow and lower body coverage in traditional draping style",

            "full-body Model in walking pose with draped garment's lower section flowing with movement, displaying how traditional draping moves naturally around legs during motion",

            "full-body Model standing on steps with draped fabric cascading down around legs, showcasing lower body traditional draping and how fabric creates elegant silhouette around lower body",

            # Draped Garment Sitting Poses - Lower Body Emphasis
            "full-body Model sitting with draped garment arranged in perfect pleats around legs, feet positioned elegantly, showcasing traditional lower body draping in seated position",

            "full-body Model sitting cross-legged with draped fabric fanned out around seated position, displaying how traditional draping adapts to floor sitting and lower body positioning",

            "full-body Model sitting on chair with draped garment flowing around legs and feet, showcasing traditional lower body coverage and draping elegance in seated pose",

            "full-body Model sitting with legs extended, draped fabric arranged along length of legs, displaying traditional lower body wrapping technique and fabric management",

            "full-body Model sitting sideways with draped garment creating elegant lines around hips and legs, showcasing traditional lower body draping from side profile view",

            # Draped Garment Movement Poses - Lower Body Focus
            "full-body Model captured mid-twirl with draped fabric spinning around legs in circular motion, displaying dynamic lower body draping and fabric movement around legs",

            "full-body Model stepping forward with draped garment flowing behind and around legs, showcasing traditional lower body draping during walking and natural movement",

            "full-body Model in dance pose with draped fabric creating beautiful lines around lower body, displaying artistic lower body draping and movement in traditional dance positions",

            "full-body Model climbing steps with draped garment managed elegantly around legs, showcasing practical lower body draping techniques during elevation changes",

            "full-body Model turning with draped fabric swirling around hips and legs, displaying traditional lower body draping during rotational body movement",

            # Lower Body Specific Poses - Leg Positioning
            "full-body Model standing with one leg extended forward through draped garment opening, showcasing traditional draping that allows for leg mobility and elegant positioning",

            "half-lower-body Model with draped garment lifted slightly to show ankle and foot positioning, displaying traditional lower body coverage while highlighting elegant leg lines",

            "full-body Model kneeling with draped garment arranged around kneeling legs, showcasing how traditional draping maintains coverage and elegance in kneeling positions",

            "full-body Model with legs positioned asymmetrically, draped fabric following leg positioning naturally, displaying traditional draping's adaptation to various leg positions",

            "full-body Model standing with weight shifted to create hip line, draped garment following body curves, showcasing traditional lower body draping that enhances natural silhouette",

            # Draped Garment Detail Poses - Lower Section Focus
            "half-lower-body Model adjusting draped garment's lower pleats and folds, hands positioned to show traditional lower body draping technique and fabric management",

            "half-lower-body Model displaying draped garment's border or hem details, positioned to highlight traditional lower garment decorative elements and craftsmanship",

            "full-body Model showing draped garment's waist to hip draping method, hands demonstrating traditional technique for lower body fabric arrangement and styling",

            "full-body Model positioned to show draped garment's layered lower construction, displaying traditional lower body layering technique and fabric arrangement methods",

            "full-body Model demonstrating traditional walking technique with draped garment, showing proper lower body movement and fabric management during traditional wear",

            # Lower Body Fabric Management Poses
            "full-body Model holding draped garment's lower edge while walking, showcasing traditional technique for managing long draped fabric around legs during movement",

            "full-body Model gathering draped garment at hip level, displaying traditional method for adjusting lower body draping length and managing fabric around legs",

            "full-body Model with draped garment tucked or pinned for practical movement, showing traditional techniques for securing lower body draping during daily activities",

            "full-body Model demonstrating traditional sitting technique, gathering draped fabric appropriately around legs before sitting, showcasing proper lower body draping etiquette",
        ]

        poses_detailed = ""
        for num, body_pose in enumerate(poses):
            body_pose = body_pose.replace('["', "").replace('"]', "").replace('"', '')
            if ".png.png" in body_pose:
                index_num = int(body_pose.split(".")[0].split("_")[-1])
                body_pose = main_poses[index_num]
            else:
                index_num = int(body_pose.split(".")[0].split("_")[-1])-1
                body_pose = fashion_poses[index_num]

            poses_detailed += f"Image {num+1}: {body_pose}\n\n"

            # body_pose = fashion_poses[int(body_pose.split(".")[0].split("_")[-1])-1]
            # poses_detailed+=f"pose_{num}: {body_pose}\n\n"

        if garment_type=="upper_garment":
            garment_detailing = f"""
                UPPER GARMENT: Use & Replicate the EXACT uploaded garment image
                - Replicate every detail from the reference image
                - Maintain identical fabrics, color, texture, and construction
                
                LOWER GARMENT SELECTION:
                - Specifications: {lower_garment_specs}
                - Style: Choose complementary fit that enhances the uploaded upper garment
                - Ensure harmonious color coordination and style balance
            """

        elif garment_type=="lower_garment":
            garment_detailing = f"""
                LOWER GARMENT: Use & Replicate the EXACT uploaded garment image
                - Replicate every detail from the reference image
                - Maintain identical fabrics, color, texture, and construction
                
                UPPER GARMENT SELECTION:
                - Specifications: {upper_garment_specs}
                - Style: Choose complementary fit that enhances the uploaded lower garment
                - Ensure harmonious color coordination and style balance
            """
        else:
            garment_detailing = """
                ONE_PIECE & DRESSES & SAREE & ETHNIC & TRADITIONAL GARMENT: Use the EXACT uploaded garment image
                - Replicate every detail from the reference image
                - Maintain identical color, texture, and construction
                - Show complete garment from neckline to hemline
            """

        # image_prompt_new = f"""
        #     Create a professional model photoshoot for all specified poses featuring the uploaded upper garment with exact replication and complementary styling.
        #
        #     GARMENT REPLICATION REQUIREMENTS:
        #     - Replicate the EXACT uploaded garment with 100% accuracy
        #     - Match fabric texture, color saturation, pattern details, weave structure
        #     - Preserve all construction elements: buttons, seams, collars, cuffs, hardware
        #     - Maintain identical fit, drape, and silhouette
        #     - Reproduce all style elements and design details precisely
        #
        #     MODEL SPECIFICATIONS:
        #     - Age: {age} years old
        #     - Gender: {gender}
        #     - Ethnicity: {ethnicity}
        #     - Garment fitting: {fitting}
        #
        #     GARMENT STYLING:
        #     {garment_detailing}
        #
        #     POSE REQUIREMENTS:
        #     Total images to generate: {len(poses)}
        #     Each pose requires a separate image with consistent styling.
        #
        #     {poses_detailed}
        #
        #     TECHNICAL SPECIFICATIONS:
        #     - Resolution: Ultra-high 4K+ quality, exactly 2160x3840 pixels
        #     - Aspect ratio: 9:16 (vertical orientation)
        #     - Professional fashion photography lighting with controlled soft shadows
        #     - Precise fabric texture rendering with authentic material draping
        #     - Color-accurate reproduction matching reference garment exactly
        #     - Sharp focus on model and garments with subtle depth of field
        #     - Professional model positioning with natural, confident body language
        #     - Accurate garment proportions and silhouette representation
        #     - Studio-quality lighting setup with proper highlight and shadow balance
        #
        #     BACKGROUND CONSISTENCY:
        #     - CRITICAL: Use the EXACT same background across ALL poses
        #     - Maintain identical background lighting, texture, and color throughout the entire photoshoot
        #     - No background variations or changes between different poses
        #     - Consistent studio backdrop or setting for visual continuity
        #     - Background should complement the garments without distraction
        #
        #     QUALITY STANDARDS:
        #     - Maintain perfect visual consistency across all poses
        #     - IDENTICAL BACKGROUND: Same backdrop, lighting, and setting in every single image
        #     - Natural, realistic appearance with professional fashion photography aesthetics
        #     - Ensure garment details are clearly visible and accurately represented
        #     - Professional retouching standards while preserving authenticity
        #     - Consistent environmental elements throughout the entire photoshoot series
        #
        #     Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
        # """

        image_prompt = f"""
            Could you please create a model photoshoot for given all poses with this given garment

            Replicate the EXACT garment from reference image - match fabric texture, color saturation, pattern details in whole garment, fit precision, style elements, Clearly shows: Button detailing and garment construction identically

            Human model age: {age} years old {gender} ({ethnicity})
            GARMENT FITTING: {fitting}
            
            CRITICAL REQUIREMENT: Generate {len(poses)} SEPARATE individual images
            - Each pose must be in its own distinct image
            - Do NOT combine multiple poses in a single image
            - Create one individual image per pose listed below
            - Total output: {len(poses)} separate image files
            
            GARMENT STYLING:
            {garment_detailing}

            INDIVIDUAL POSE REQUIREMENTS:
            Generate the following poses as SEPARATE images:
            {poses_detailed}
            
            BACKGROUND CONSISTENCY:
            - CRITICAL: Use the EXACT same background across ALL separate poses images
            - Maintain identical background lighting, texture, and color throughout the entire photoshoot
            - No background variations or changes between different poses
            - Consistent studio backdrop or setting for visual continuity
            - Background should complement the garments without distraction

            TECHNICAL SPECIFICATIONS:
            - Use exact same lower garment type
            - Use exact same upper garment type
            - Ultra-high resolution (4K+), **specifically 2160x3840 pixels**, photorealistic quality
            - **Aspect ratio: 9:16 (vertical)**
            - Professional fashion photography lighting with soft shadows
            - Precise fabric texture rendering and authentic draping
            - Color-accurate reproduction matching reference materials
            - Sharp focus on model and garments with depth of field
            - Professional model positioning and natural body language
            - Accurate garment length and silhouette representation

            Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
        """

        parts = []
        if upper_garment_image:
            exten = upper_garment_image.split(".")[-1]
            if exten.lower() in ["jpg", "jpeg"]:
                exten = "jpeg"
            upper_garment_path = f"static/photoshoots_folders/{photoshoot_id}/{upper_garment_image}"
            with open(upper_garment_path, "rb") as f:
                upper_image_data = f.read()

            parts.append(types.Part.from_bytes(
                mime_type=f"image/{exten.lower()}",
                data=upper_image_data,
            ))

        if below_garment_image:
            exten = below_garment_image.split(".")[-1]
            if exten.lower() in ["jpg", "jpeg"]:
                exten = "jpeg"
            lower_garment_path = f"static/photoshoots_folders/{photoshoot_id}/{below_garment_image}"
            with open(lower_garment_path, "rb") as f:
                lower_image_data = f.read()

            parts.append(types.Part.from_bytes(
                mime_type=f"image/{exten.lower()}",
                data=lower_image_data,
            ))

        parts.append(types.Part.from_text(text=image_prompt))

        client = genai.Client(
            api_key="AIzaSyBXyMioJM4k5YLKsYx6VkrZ6VSztsERC0w",
        )

        model_gemini = "gemini-2.5-flash-image-preview"

        contents = [
            types.Content(
                role="user",
                parts=parts,
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            response_modalities=[
                "IMAGE",
                "TEXT",
            ]
        )

        response = client.models.generate_content(
            model=model_gemini,
            contents=contents,
            config=generate_content_config
        )

        file_index = 0
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                file_index += 1
                image = Image.open(BytesIO(part.inline_data.data))
                output_filename = f"{uuid.uuid4()}_photoshoot_{file_index}.png"
                filename=f"static/photoshoots_folders/{photoshoot_id}/{output_filename}"
                image.save(filename)
                all_generated_images.append(output_filename)

        total_credit = len(all_generated_images)

        user_id = garment_mapping_dict.get("id")
        user_data = list(mongoOperation().get_spec_data_from_coll("company_data", {"id": user_id}))

        if user_data:
            user_credit = int(user_data[0]["credit"])
            remaining_credit = user_credit - total_credit
            mongoOperation().update_mongo_data("company_data", {"id": user_id}, {"credit": remaining_credit})

        all_images = garment_mapping_dict.get("all_images", [])
        for images in all_generated_images:
            base_url = constant_dict.get('domain_url', 'http://localhost:8060')  # Your domain
            garment_image_url = f"{base_url}/static/photoshoots_folders/{photoshoot_id}/{images}"
            all_images.append(garment_image_url)

        photoshoot_mapping = {
            "is_credit_debited": True,
            "is_completed": True,
            "total_credit": total_credit,
            "all_images": all_images,
            "status": "completed"
        }

        mongoOperation().update_mongo_data("photoshoot_data", {"id": user_id, "photoshoot_id": photoshoot_id},
                                           photoshoot_mapping)

        return {
            'status': 'completed',
            'total_images': len(all_generated_images),
            'total_credit': total_credit,
            'all_images': all_images
        }

    except Exception as e:
        print(f"Error in background task: {e}")
        # Update status to failed
        mongoOperation().update_mongo_data(
            "photoshoot_data",
            {"id": garment_mapping_dict.get("id"), "photoshoot_id": photoshoot_id},
            {"status": "failed", "error": str(e)}
        )
        return {}
