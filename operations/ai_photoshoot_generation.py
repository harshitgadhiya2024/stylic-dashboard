import base64
import random
import uuid

from flask import url_for, session
from openai import OpenAI
import os
from PIL import Image

from operations.mail_sending import emailOperation
from operations.mongo_operation import mongoOperation
from operations.prompt_generator import generate_fashion_prompt, single_generate_fashion_prompt
from utils.constant import constant_dict
from utils.html_format import htmlOperation

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
                                        lower_garment_filename):
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

        generator = GarmentPhotoshootGenerator()
        age_group = garment_mapping_dict.get("age_group")
        gender = garment_mapping_dict.get("gender")
        ethnicity = garment_mapping_dict.get("ethnicity")
        height = garment_mapping_dict.get("height")
        fitting = garment_mapping_dict.get("fitting")
        weight = garment_mapping_dict.get("width")
        muscle_tone = "toned"
        standing_pose = "confident"
        facial_expression = "smile"
        lighting = "natural"
        background_view = "outdoor"
        age = garment_mapping_dict.get("age")

        # Compose descriptions
        model_type = f"{age_group} {ethnicity} {gender} ({age} years old)"
        background = f"{background_view} with {lighting} lighting"
        body_type = f"{standing_pose} with {facial_expression} expression"
        body_structure = f"height: {height}, weight: {weight}, muscle tone: {muscle_tone}"
        model_description = f"{model_type}, {body_type}, {body_structure}"
        poses = garment_mapping_dict.get("selected_poses", [])

        all_generated_images = []

        face_params = {
            "hair": {
                "color": "black",
            },
            "skin": {
                "tone": "light",
                "texture": "smooth"
            },
            "age_group": age_group,
            "age": age,
            "gender": gender,
            "expression": "neutral",
            "ethnicity": ethnicity,
            "lighting": "soft natural light"
        }
        garment_type = garment_mapping_dict.get("upload_garment_type")

        # Generate face
        face_photo_url = ""
        if age_group in ['infant', 'toddler', 'young-child', 'pre-teen', 'early-teen']:
            pass
        elif len(poses) > 1 and garment_type!="lower_garment":
            photo_file_name = f"{uuid.uuid4()}generatedface.png"
            face_photo_url = generator.generate_model_face(face_params, photo_file_name, photoshoot_id)

            # Fix the logic issue with face generation loop
            while not face_photo_url:  # Changed from "while face_photo_url:" which was incorrect
                face_photo_url = generator.generate_model_face(face_params, photo_file_name, photoshoot_id)
            # all_generated_images.append(photo_file_name)
        else:
            pass

        mongoOperation().update_mongo_data(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id},
            {"status": "masking_generated"}
        )


        upper_garment_image = upper_garment_filename
        below_garment_image = lower_garment_filename
        upper_garment_category = garment_mapping_dict.get("upper_garment_type")
        below_garment_category = garment_mapping_dict.get("lower_garment_type")

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

        for num, body_pose in enumerate(poses):
            body_pose = body_pose.replace('["', "").replace('"]', "").replace('"', '')
            body_pose = fashion_poses[int(body_pose.split(".")[0].split("_")[-1])-1]
            print(body_pose)
            sample_params = {
                'age_group': age_group,
                'gender': gender,
                'ethnicity': ethnicity,
                'height': height,
                'weight': weight,
                'fitting': fitting,
                'age': age,
                'upper_garment_type': upper_garment_category,
                'lower_garment_type': below_garment_category,
                'pose': body_pose
            }
            if age_group in ['infant', 'toddler', 'young-child', 'pre-teen', 'early-teen']:
                print("coming to children")
                image_prompt = single_generate_fashion_prompt(garment_type, sample_params)

                output_filename = f"{uuid.uuid4()}_photoshoot_{num + 1}.png"
                result = generator.single_generate_photoshoot_image(
                    photoshoot_id, image_prompt, face_photo_url, garment_type, upper_garment_image, below_garment_image,
                    output_filename
                )
            elif len(poses)>1:
                print("coming to multi photo")
                image_prompt = generate_fashion_prompt(garment_type, sample_params)

                output_filename = f"{uuid.uuid4()}_photoshoot_{num + 1}.png"
                result = generator.generate_photoshoot_image(
                    photoshoot_id, image_prompt, face_photo_url, garment_type, upper_garment_image, below_garment_image,
                    output_filename
                )
            else:
                print("coming to single photo")
                image_prompt = single_generate_fashion_prompt(garment_type, sample_params)

                output_filename = f"{uuid.uuid4()}_photoshoot_{num + 1}.png"
                result = generator.single_generate_photoshoot_image(
                    photoshoot_id, image_prompt, face_photo_url, garment_type, upper_garment_image, below_garment_image,
                    output_filename
                )


            if result:
                all_generated_images.append(output_filename)
                print(f"Successfully generated: {result}")
            else:
                print(f"Failed to generate image for pose: {body_pose}")

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
            # garment_image_url = url_for('static',
            #                                   filename=f'photoshoots_folders/{photoshoot_id}/{images}',
            #                                   _external=True)
            # garment_image_url = f"{constant_dict.get('domain_url')}/static/photoshoots_folders/{photoshoot_id}/{images}"
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
