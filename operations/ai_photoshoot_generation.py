import subprocess
from operations.mongo_operation import mongoOperation
from utils.constant import constant_dict
import os, uuid

from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types


def generate_model_face(face_params, output_filename, photoshoot_id):
    """Generate a consistent model face based on parameters"""
    try:
        prompt = create_face_prompt(face_params)
        print(f"Generating face with prompt: {prompt}")
        generate_content_config = types.GenerateContentConfig(
            response_modalities=[
                "IMAGE",
                "TEXT",
            ]
        )
        client = genai.Client(
            api_key="AIzaSyBXyMioJM4k5YLKsYx6VkrZ6VSztsERC0w",
        )

        model_gemini = "gemini-2.5-flash-image-preview"
        parts = []
        parts.append(types.Part.from_text(text=prompt))
        base_contents = [
            types.Content(
                role="user",
                parts=parts,
            ),
        ]

        response = client.models.generate_content(
            model=model_gemini,
            contents=base_contents,
            config=generate_content_config
        )

        for part in response.candidates[0].content.parts:
            if part.text is not None:
                print(part.text)
            elif part.inline_data is not None:
                image = Image.open(BytesIO(part.inline_data.data))
                image_path = f"static/photoshoots_folders/{photoshoot_id}/{output_filename}"
                image.save(image_path)

        return output_filename

    except Exception as e:
        print(f"Error generating face: {e}")
        return None

def create_face_prompt(params):
    """Create detailed face generation prompt"""
    try:
        prompt_parts = []

        # Basic description
        prompt_parts.append(
            f"{params['ethnicity']} headshot portrait of a {params['age']} years of {params['gender']} person")

        # Hair
        hair_desc = f"{params['hair']['color']} hair color"
        prompt_parts.append(hair_desc)

        # Skin
        prompt_parts.append(f"{params['skin']['tone']} {params['skin']['texture']} skin")

        # Expression and lighting
        prompt_parts.append(f"{params['expression']} expression")
        prompt_parts.append(f"photographed with {params['lighting']}")

        # Quality descriptors
        prompt_parts.append("high resolution, photorealistic, clean background, Don't wear anything only give face image")

        return ", ".join(prompt_parts)

    except Exception as e:
        print(f"Error creating face prompt: {e}")
        return ""

def calculate_estimated_cost(num_poses, has_upper_garment=True, has_lower_garment=True):
    """
    Calculate estimated cost for photoshoot generation
    """
    # Base costs per request
    text_input_cost_per_1k_tokens = 0.000075
    text_output_cost_per_1k_tokens = 0.0003
    image_input_cost = 0.00315
    estimated_image_generation_cost = 0.04

    # Estimate tokens per request
    avg_input_tokens = 500
    avg_output_tokens = 100

    # Calculate input images per request
    garment_images = (1 if has_upper_garment else 0) + (1 if has_lower_garment else 0)

    # Base request cost
    base_request_cost = (
            (avg_input_tokens * text_input_cost_per_1k_tokens / 1000) +
            (avg_output_tokens * text_output_cost_per_1k_tokens / 1000) +
            (garment_images * image_input_cost) +
            estimated_image_generation_cost
    )

    # Subsequent requests include reference image
    subsequent_request_cost = base_request_cost + image_input_cost

    # Total cost calculation
    total_requests = num_poses
    if num_poses > 1:
        total_cost = base_request_cost + ((num_poses - 1) * subsequent_request_cost)
    else:
        total_cost = base_request_cost

    return {
        'total_requests': total_requests,
        'estimated_total_cost': round(total_cost, 4),
        'cost_per_image': round(total_cost / num_poses, 4),
        'base_request_cost': round(base_request_cost, 4),
        'subsequent_request_cost': round(subsequent_request_cost, 4)
    }


def upscale_image(input_image: str, output_image: str):
    try:
        # Ensure the binary has execute permission
        # subprocess.run(["chmod", "u+x", "realesrgan-ncnn-vulkan"], check=True)

        # Run realesrgan with input and output
        subprocess.run(
            ["./realesrgan-ncnn-vulkan", "-i", input_image, "-o", output_image, "-n", "realesrgan-x4plus"],
            check=True
        )
        return True
    except:
        return False

def generate_photoshoot_background_task(garment_mapping_dict, photoshoot_id, upper_garment_filename,
                                        lower_garment_filename, lower_garment_type, upper_garment_type, lower_garment_specs, upper_garment_specs, garment_type, background_description, selected_background=None):
    """
    Background task for generating photoshoot images
    """
    try:
        # Update status to processing
        user_id = garment_mapping_dict.get("id")
        all_generated_images = []
        mongoOperation().update_mongo_data(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id},
            {"status": "processing"}
        )

        gender = garment_mapping_dict.get("gender")
        height = garment_mapping_dict.get("height")
        weight = garment_mapping_dict.get("weight")
        age_group = garment_mapping_dict.get("age_group")
        ethnicity = garment_mapping_dict.get("ethnicity")
        fitting = garment_mapping_dict.get("fitting")
        age = garment_mapping_dict.get("age")
        poses = garment_mapping_dict.get("selected_poses", [])
        pose_input_method = garment_mapping_dict.get("pose_input_method", "predefined")
        pose_descriptions = garment_mapping_dict.get("pose_descriptions", [])
        upper_garment_image = upper_garment_filename
        below_garment_image = lower_garment_filename

        fashion_poses = [
            "full body standing straight facing camera, hands on hips, confident look",
            "full body relaxed stance, one leg slightly forward, arms crossed, looking to side",
            "full body standing with one arm raised, leaning slightly back",
            "full body walking forward mid-stride, natural motion",
            "half right side angle upper body standing sideways, looking over shoulder",
            "full body leaning slightly on wall, hands in pockets",
            "full body arms crossed behind back",
            "full body one hand on waist",
            "half upper body front view slightly looking down",
            "full body standing on one leg with the other bent, playful posture",
            "full body sitting on stool, one leg crossed over the other, hands on lap, straight back",
            "full body leaning forward on knees, elbows on thighs",
            "full body lounging, legs extended, arm behind head",
            "full body sitting sideways, chin resting on hand",
            "full body sitting cross-legged on floor, looking up slightly",
            "full body seated on high chair, legs crossed, arms resting casually",
            "full body one knee up, seated, elbows resting on knee",
            "full body reclining slightly on floor with one arm supporting upper body",
            "full body sitting on window ledge",
            "full body sitting backwards on chair, arms resting on backrest",
            "full body high-fashion stance, one foot forward, hips tilted",
            "full body in motion",
            "full body asymmetrical pose, arm lifted",
            "full body power pose, hands on waist, wide-legged stance",
            "full body leaning dramatically to side",
            "full body crouching low with head turned toward camera",
            "full body twirling or spinning motion",
            "full body arms spread out, walking with confidence",
            "full body interacting naturally with prop",
            "half lower body standing with legs shoulder-width apart",
            "half lower body one leg stepped forward",
            "half lower body walking stride",
            "half lower body weight on one leg",
            "half lower body sitting on stool with legs crossed",
            "half lower body leaning against wall",
            "half lower body hands in pockets",
            "half lower body lunging position",
            "half lower body standing on stairs",
            "half lower body one foot on elevated surface",
            "half upper body front view standing straight with hands on hips",
            "half upper body front view arms crossed",
            "half upper body front view adjusting collar with one hand",
            "half upper body front view one arm raised above head",
            "half upper body front view leaning slightly forward, hands clasped behind back",
            "half upper body front view arms extended sideways",
            "half upper body front view holding lapels",
            "half upper body front view one hand on shoulder, other on waist",
            "half upper body front view adjusting cufflinks or sleeves",
            "half upper body front view arms crossed at chest level",
            "full body standing with drape arranged",
            "full body formal stance",
            "full body with drape in motion",
            "half upper body front view adjusting strap",
            "full body sitting gracefully",
            "full body hands clasped",
            "full body walking in motion",
            "full body spinning",
            "half upper body front view adjusting jewelry",
            "full body outdoors with flowing motion",
            "full body standing straight with arms at sides",
            "full body one hand on hip, other adjusting strap",
            "full body playful stance with legs apart",
            "full body walking with fabric in motion",
            "full body hands in pockets, casual stance",
            "full body stretching pose",
            "full body spinning with flowing motion",
            "full body power pose with wide stance",
            "full body adjusting wrap tie",
            "full body arms extended",
            "full body standing straight facing camera with hands on hips, confident look",
            "full body relaxed stance with one leg slightly forward, arms crossed, looking to side",
            "full body standing with one arm raised, leaning slightly back",
            "full body walking forward mid-stride, natural motion",
            "half right side angle upper body standing sideways looking over shoulder",
            "full body leaning slightly on wall with hands in pockets",
            "full body arms crossed behind back",
            "full body one hand on waist",
            "half upper body front view looking down",
            "full body standing on one leg with other bent, playful posture"
        ]
        main_poses = [
   # Front Standing Poses
   "half upper body front view standing straight facing camera, arms relaxed at sides, shoulders back, chin slightly raised, direct eye contact",

   "half upper body front view three-quarter stance, one hand on hip, other arm hanging naturally, weight shifted to one leg",

   "half upper body front view standing with arms crossed casually over chest, confident expression, shoulders slightly forward",

   "half upper body front view hands clasped behind back, chest open, standing tall with perfect posture",

   "half upper body front view reaching one arm across body to opposite shoulder, other arm relaxed, creating diagonal lines",

   # Back Standing Poses
   "half back view upper body standing with back to camera, looking over shoulder, arms at sides",

   "half back view upper body facing away from camera, arms crossed behind back, head turned slightly to show profile",

   "half back view upper body with back to camera, one hand running through hair, other arm extended slightly",

   "half back view upper body standing with back facing camera, both arms raised touching back of neck/head",

   "half back view upper body leaning against wall with one shoulder, arms relaxed",

   # Side Profile Poses
   "half right side angle upper body perfect side profile, chin raised, arms positioned naturally at sides",

   "half left side angle upper body side stance with arms crossed, looking straight ahead",

   "half right side angle upper body three-quarter back view, slight turn toward camera, one hand on hip",

   # Sitting Poses - Front Focus
   "half upper body front view sitting forward on edge of seat, elbows resting on knees, leaning toward camera",

   "half upper body front view sitting relaxed with one arm draped over chair back, other hand on leg",

   "half upper body front view sitting cross-legged, hands resting on ankles, straight posture",

   # Sitting Poses - Back Focus
   "half back view upper body sitting facing away from camera on chair, looking back over shoulder, arms resting naturally",

   "half back view upper body sitting sideways on chair, both arms on chair back, looking toward camera",

   # Dynamic Movement Poses
   "half upper body front view captured mid-stride walking toward camera, arms naturally swinging",

   "half upper body front view turning motion, arms slightly outstretched",

   "half upper body front view stepping forward with one foot, arms positioned in natural walking gesture",

   # Arm Positioning - Front Focus
   "half upper body front view both hands running through hair, elbows raised, eyes looking up",

   "half upper body front view one hand touching neck/collar area gently, other arm relaxed at side",

   "half upper body front view arms stretched overhead",

   "half upper body front view adjusting sleeves or cuffs with focused downward gaze",

   # Arm Positioning - Back Focus
   "half back view upper body facing away with both arms raised above head",

   "half back view upper body with back to camera, one hand touching opposite shoulder blade, other arm relaxed",

   "half back view upper body facing away, arms positioned as if stretching or reaching",

   # Leaning and Support Poses
   "half upper body front view leaning against wall with one shoulder, arms crossed, relaxed expression",

   "half upper body front view leaning back against surface with arms at sides",

   "half upper body front view leaning forward slightly, hands on hips",

   # Interactive Lifestyle Poses
   "half upper body front view reaching up toward something above",

   "half upper body front view positioned as if adjusting details, hands naturally interacting",

   "half upper body front view casual pose suggesting everyday wear, arms positioned naturally for daily activities",

   # Close-up Upper Body Focus
   "zoomed detail view upper body shot with arms positioned to frame torso",

   "zoomed detail view one arm across body, hand resting on opposite arm, creating interesting lines",

   "zoomed detail view hands clasped in front, arms creating frame",

   # Back Detail Poses
   "half back view upper body with back three-quarters to camera, one arm reaching across to opposite shoulder",

   "half back view upper body facing completely away, arms hanging naturally, perfect back view",

   "half back view upper body with back to camera, hands on hips, elbows out",

   # Front Standing Poses - Full Body
   "full body standing straight facing camera, arms relaxed at sides, feet shoulder-width apart",

   "full body confident stance, one hand on hip, other arm hanging naturally, weight shifted to one leg",

   "full body standing, arms crossed casually over chest, legs positioned naturally",

   "full body standing with hands clasped behind back, chest open and shoulders back",

   "full body reaching one arm across body to opposite shoulder, creating diagonal lines",

   # Back Standing Poses - Full Body
   "full body back view standing with back to camera, looking over shoulder",

   "full body back pose facing away, arms crossed behind back, legs positioned naturally",

   "full body back to camera, one hand running through hair, other arm extended",

   "full body back view standing, both arms raised touching back of neck",

   "full body back pose leaning against wall with one shoulder",

   # Side Profile Poses - Full Body
   "full body side profile with chin raised, arms positioned naturally",

   "full body side view in confident stance, arms crossed",

   "full body three-quarter back view, slight turn toward camera, one hand on hip",

   # Chair and Furniture Poses
   "full body sitting on modern chair, leaning back with one leg crossed over the other, arms draped naturally on armrests",

   "full body perched on edge of desk or table, legs dangling, hands gripping edge for support",

   "full body sitting backwards on chair, straddling seat, arms resting on chair back, facing camera",

   "full body lounging in oversized armchair, one leg tucked under, other foot on floor, arm draped over chair arm",

   "full body sitting on bar stool or high chair, feet resting on footrest, hands on knees",

   "full body sitting sideways on bench, one leg up on bench, other foot on ground, hands positioned naturally",

   # Sunglasses Poses
   "full body standing confidently with hands on hips",

   "full body one hand adjusting sunglasses pushed up on head, other arm relaxed",

   "full body arms crossed casually, leaning against wall",

   "full body one hand on hip, other hand free",

   "full body arms raised to face",

   # Bag and Purse Poses
   "full body one arm relaxed at side, other holding prop",

   "full body hands positioned naturally",

   "full body adjusting or looking through contents",

   "full body both hands extended slightly",

   "full body one hand holding strap, other hand free",

   # Lighting and Lamp Props
   "full body arms extended, interacting with prop",

   "full body positioned near prop, one hand touching or adjusting",

   "full body arms arranged to display prop",

   "full body hands cupped around prop",

   # Book and Reading Props
   "full body sitting with open book in lap, one hand holding pages, other arm resting naturally",

   "full body standing while reading book, holding it with both hands",

   "full body holding stack against chest with one arm, other hand free",

   "full body sitting cross-legged on floor with book open, leaning over to read",

   # Coffee and Beverage Props
   "full body holding cup or mug with both hands near chest",

   "full body sitting at table, one hand on cup handle, other arm resting on table",

   "full body holding bottle or drink, about to take sip",

   "full body raising cup in toast gesture, other hand on hip",

   # Phone and Technology Props
   "full body holding smartphone, looking at screen",

   "full body talking on phone, one hand holding device to ear, other arm gesturing naturally",

   "full body sitting with laptop on lap, hands on keyboard",

   "full body holding tablet, looking at screen",

   # Flower and Plant Props
   "full body holding bouquet with both hands, positioned near chest area",

   "full body smelling single flower, holding it delicately near face, other arm relaxed",

   "full body sitting near or tending to potted plant, hands interacting with leaves or pot",

   "full body holding small succulent or plant pot, arms positioned naturally",

   # Music and Instrument Props
   "full body holding acoustic guitar, hands positioned on strings and neck",

   "full body with headphones around neck or on head, hands adjusting them",

   "full body holding vinyl record or CD, examining it",

   # Art and Creative Props
   "full body holding paintbrush or art supplies, hands positioned as if creating",

   "full body sitting at easel or art station, hands working with creative materials",

   "full body holding camera, positioned as if taking photos",

   "full body with art palette or sketchbook, hands positioned for creative work",

   # Mirror and Reflection Props
   "full body looking in handheld mirror, one hand holding mirror, other touching face or hair",

   "full body positioned near full-length mirror, looking at reflection",

   "full body holding compact mirror, checking reflection, other hand free",

   # Food and Kitchen Props
   "full body holding piece of fruit or small snack, positioned near mouth",

   "full body sitting at kitchen counter, hands interacting with food props",

   "full body holding cooking utensil or kitchen tool, positioned as if preparing food",

   # One-Piece Garment Specific Poses - Standing
   "full body standing with arms raised above head in celebration pose",

   "full body asymmetrical standing pose, one hip jutted out, arms positioned at different heights",

   "full body standing with one leg stepped forward, hands on waist",

   "full body twisting motion, body turned at waist, arms following the movement",

   "full body standing with arms stretched wide",

   # One-Piece Garment Specific Poses - Sitting
   "full body sitting on floor with legs extended straight, leaning back on hands",

   "full body sitting cross-legged with perfect posture, hands resting on ankles",

   "full body sitting on chair with legs tucked to one side",

   "full body sitting sideways on chair or stool, one leg hanging down, other tucked up",

   "full body perched on chair arm or elevated surface, both legs dangling",

   # One-Piece Garment Specific Poses - Movement
   "full body captured mid-spin with arms outstretched",

   "full body walking motion with exaggerated step",

   "full body jumping or leaping with arms and legs positioned dynamically",

   "full body dance-inspired pose with fluid arm and leg positioning",

   "full body stepping up onto platform or step, one leg raised",

   # One-Piece Garment Specific Poses - Stretching
   "full body reaching upward with both arms, body extended vertically",

   "full body side stretch pose, one arm reaching over head to opposite side",

   "full body bending forward slightly with arms hanging naturally",

   "full body back arch pose with hands on lower back, chest open",

   # One-Piece Garment Specific Poses - Lying Down
   "full body lying on side with legs stacked, head propped on hand",

   "full body lying on back with arms stretched overhead",

   "full body casual reclined position against pillows or cushions",

   # One-Piece Garment Specific Poses - Hands on Garment
   "full body smoothing or adjusting at waist area",

   "full body holding or lifting hem slightly",

   "full body adjusting neckline or shoulder area",

   "full body hands positioned naturally",

   # Traditional Draped Garment Poses - Standing
   "full body standing in classic pose with drape arranged elegantly over one shoulder, other arm gracefully positioned at waist",

   "full body regal standing position with drape flowing behind, one hand holding fabric edge delicately",

   "full body standing with drape wrapped around torso, arms positioned naturally",

   "full body confident stance with pleats arranged perfectly, one hand adjusting drape at shoulder",

   "full body standing with drape creating elegant silhouette, both arms positioned naturally",

   # Traditional Draped Garment Poses - Movement
   "full body captured mid-twirl with drape spinning outward, creating circular motion",

   "full body walking pose with drape flowing behind in graceful movement",

   "full body stepping gracefully with one foot forward, drape arranged in elegant folds",

   "full body dance-inspired pose with drape creating beautiful lines, arms positioned naturally",

   "full body turning with drape following body movement",

   # Traditional Fitted Top and Flared Bottom Combination Poses
   "full body standing with arms raised, flared lower section displayed in full circular spread around legs",

   "full body spinning motion with fitted top maintaining shape while flared bottom creates dramatic circle",

   "full body sitting on floor, flared bottom arranged in elegant circle around seated position",

   "full body dancing pose, flared bottom capturing motion",

   "full body standing on elevated surface, flared bottom cascading down",

   # Traditional Ethnic Ensemble Poses - Three-Piece Coordination
   "full body standing with arms positioned naturally",

   "full body twirling motion",

   "full body sitting gracefully",

   "full body profile pose",

   "full body standing with hands positioned to adjust or display",

   # Traditional Formal Dress Poses - Full Length
   "full body standing regally, arms positioned gracefully",

   "full body walking, fabric flowing naturally",

   "full body seated formally, arranged elegantly around chair",

   "full body formal pose, arms and posture reflecting traditional etiquette",

   "full body standing, one hand lifting fabric edge slightly",

   # Traditional Garment Detail Poses
   "full body adjusting draping or pleating, hands delicately positioned",

   "full body positioning arms and body naturally",

   "full body hands positioned to demonstrate layering",

   "full body pose that displays construction details",

   "full body demonstrating versatility by adjusting draping or styling",

   # Traditional Garment Sitting Poses
   "full body sitting cross-legged on floor, arranged in elegant circle",

   "full body sitting on traditional low seating, flowing naturally",

   "full body sitting sideways, draped elegantly",

   "full body sitting with layers arranged carefully",

   "full body formal sitting pose, presented properly",

   # Additional Ethnic Wear Poses - Regional Variations
   "full body standing, arms positioned naturally",

   "full body traditional cultural greeting pose",

   "full body walking, flowing in traditional manner",

   "full body seated in traditional cultural posture",

   "full body demonstrating traditional cultural dance movement",

   # Ethnic Wear with Traditional Accessories Integration
   "full body adjusting head covering or veil, hands positioned naturally",

   "full body standing pose",

   "full body arms arranged naturally",

   "full body holding prop",

   "full body pose, hands positioned naturally",

   # Ethnic Wear Ceremonial and Festival Poses
   "full body celebratory pose, arms raised in traditional celebration gesture",

   "full body kneeling in traditional ceremonial position",

   "full body traditional prayer or meditation pose",

   "full body performing traditional offering gesture, hands positioned in cultural greeting or blessing pose",

   "full body traditional wedding or celebration pose",

   # Ethnic Wear Layering and Draping Techniques
   "full body demonstrating traditional layering technique, hands positioned naturally",

   "full body adjusting traditional wrap or shawl, hands positioned naturally",

   "full body with traditional layering or draping adjusted",

   "full body pose displaying modular construction",

   "full body demonstrating traditional wearing style",

   # Ethnic Wear Intergenerational and Cultural Continuity Poses
   "full body pose reflecting traditional cultural values, posture and hand positioning naturally",

   "full body displaying traditional age-appropriate styling",

   "full body educational pose, positioned naturally",

   "full body everyday versus ceremonial presentation",

   "full body pose that bridges traditional and contemporary styling",

   # Draped Garment Standing Poses - Lower Body Focus
   "half lower body standing with drape flowing around legs, one foot slightly forward",

   "half lower body confident stance with drape arranged around hips and thighs, hands adjusting lower drape",

   "half lower body standing with drape's lower portion spread elegantly, legs positioned naturally",

   "half lower body walking pose with drape's lower section flowing with movement",

   "half lower body standing on steps with drape cascading down around legs",

   # Draped Garment Sitting Poses - Lower Body Emphasis
   "half lower body sitting with drape arranged in perfect pleats around legs, feet positioned elegantly",

   "half lower body sitting cross-legged with drape fanned out around seated position",

   "half lower body sitting on chair with drape flowing around legs and feet",

   "half lower body sitting with legs extended, drape arranged along length of legs",

   "half lower body sitting sideways with drape creating elegant lines around hips and legs",

   # Draped Garment Movement Poses - Lower Body Focus
   "half lower body captured mid-twirl with drape spinning around legs in circular motion",

   "half lower body stepping forward with drape flowing behind and around legs",

   "half lower body dance pose with drape creating beautiful lines around lower body",

   "half lower body climbing steps with drape managed elegantly around legs",

   "half lower body turning with drape swirling around hips and legs",

   # Lower Body Specific Poses - Leg Positioning
   "half lower body standing with one leg extended forward",

   "half lower body with drape lifted slightly to show ankle and foot positioning",

   "half lower body kneeling with drape arranged around kneeling legs",

   "half lower body with legs positioned asymmetrically, drape following leg positioning naturally",

   "half lower body standing with weight shifted to create hip line, drape following body curves",

   # Draped Garment Detail Poses - Lower Section Focus
   "half lower body adjusting drape's lower pleats and folds, hands positioned naturally",

   "half lower body displaying drape's border or hem details",

   "half lower body showing drape's waist to hip draping method, hands demonstrating technique",

   "half lower body positioned to show drape's layered lower construction",

   "half lower body demonstrating traditional walking technique with drape",

   # Lower Body Fabric Management Poses
   "half lower body holding drape's lower edge while walking",

   "half lower body gathering drape at hip level",

   "half lower body with drape tucked or pinned for practical movement",

   "half lower body demonstrating traditional sitting technique, gathering drape appropriately around legs before sitting",
]

        client = genai.Client(
            api_key="AIzaSyBXyMioJM4k5YLKsYx6VkrZ6VSztsERC0w",
        )

        model_gemini = "gemini-2.5-flash-image-preview"

        generate_content_config = types.GenerateContentConfig(
            response_modalities=[
                "IMAGE",
                "TEXT",
            ]
        )

        photo_file_name = f"{uuid.uuid4()}generatedface.png"

        # face_params = {
        #     "hair": {
        #         "color": "black",
        #     },
        #     "skin": {
        #         "tone": "light",
        #         "texture": "smooth"
        #     },
        #     "age_group": age_group,
        #     "age": age,
        #     "gender": gender,
        #     "expression": "neutral",
        #     "ethnicity": ethnicity,
        #     "lighting": "soft natural light"
        # }
        #
        # face_photo_url = generate_model_face(face_params, photo_file_name, photoshoot_id)
        # while not face_photo_url:
        #     face_photo_url = generate_model_face(face_params, photo_file_name, photoshoot_id)
        #     print("Retrying face generation...")

        # face_photo_url = f"static/photoshoots_folders/{photoshoot_id}/{face_photo_url}"
        mongoOperation().update_mongo_data(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id},
            {"status": "masking_generated"}
        )

        # Handle background description - use selected background image if provided
        final_background_description = background_description
        if selected_background:
            final_background_description = f"Use the exact same background from the provided background image."
        elif background_description:
            final_background_description = background_description
        else:
            final_background_description = "Professional studio background with soft, even lighting that complements the garment"

        body_poses = []
        if pose_input_method == "predefined":
            # Original predefined poses logic
            for num, body_pose in enumerate(poses):
                body_pose = body_pose.replace('["', "").replace('"]', "").replace('"', '')
                if ".png.webp" in body_pose:
                    index_num = int(body_pose.split(".")[0].split("_")[-1])
                    body_pose = main_poses[index_num]
                else:
                    index_num = int(body_pose.split(".")[0].split("_")[-1])-1
                    body_pose = fashion_poses[index_num]
                body_poses.append(body_pose)
        elif pose_input_method == "upload" or pose_input_method == "prompts":
            # Use the analyzed pose descriptions directly
            body_poses = pose_descriptions if pose_descriptions else []

        garmentdescription = ""
        if upper_garment_specs:
            garmentdescription+=f" Upper garment details: {upper_garment_specs}"
        if lower_garment_specs:
            garmentdescription+=f" Lower garment details: {lower_garment_specs}"

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

        generated_first_image_path = ""
        for unique_num, pose_detail in enumerate(body_poses):
            if unique_num==0:
                if selected_background:
                    try:
                        background_image_path = f"static/background_images/{selected_background}"
                        if os.path.exists(background_image_path):
                            with open(background_image_path, "rb") as f:
                                background_image_data = f.read()
                            parts.append(types.Part.from_bytes(
                                mime_type="image/webp",
                                data=background_image_data,
                            ))
                            print(f"Added background image: {selected_background}")
                        else:
                            print(f"Background image not found: {background_image_path}")
                    except Exception as e:
                        print(f"Error loading background image: {e}")

                image_prompt = f'''
                    Create a professional fashion photoshoot image of a {age} years {age_group} old {ethnicity} {gender} wearing the specified outfit with given garment.
    
                    CRITICAL REQUIREMENTS:
                    1. BACKGROUND: Use the EXACT background from the reference background image - preserve all characteristics with 100% accuracy
                    2. OUTFIT COORDINATION: Ensure both garments work harmoniously together while maintaining their individual reference accuracy
    
                    GARMENT REQUIREMENTS:
                    - CRITICAL: Exact replication of reference garment required
                    - Match all design elements with 100% accuracy:
                      * Fabric texture and weave pattern
                      * Color saturation and tone precision
                      * Pattern details and placement
                      * Garment construction and seaming
                      * Style elements and embellishments
                      * Fit characteristics: Regular fit silhouette
                    - Don't add any design or modifications in garment by your self
                    - NO creative interpretation or modifications allowed
                    - Maintain authentic draping and fabric behavior
          
                    MODEL SPECIFICATIONS (MUST REMAIN CONSISTENT):
                    - Age: {age} years ({age_group})
                    - Ethnicity: {ethnicity}
                    - Gender: {gender}
                    - Height: {height}
                    - Build: {weight}
                    - Professional fashion model appearance with natural, authentic expression
    
                    GARMENT SPECIFICATIONS (EXACT REPLICATION REQUIRED):
                    {garmentdescription}
                    
                    BACKGROUND SPECIFICATIONS (EXACT REPLICATION REQUIRED):
                    {final_background_description}
    
                    POSE SPECIFICATIONS (EXACT REPLICATION REQUIRED):
                    {pose_detail}
    
                    TECHNICAL SPECIFICATIONS:
                    - Ultra-high resolution (4K+), photorealistic quality
                    - Professional fashion photography lighting with soft shadows
                    - Precise fabric texture rendering and authentic draping for both pieces
                    - Color-accurate reproduction matching all reference materials
                    - Sharp focus on model and both garments with depth of field
                    - Professional model positioning and natural body language
                    - Seamless integration of all reference elements
    
                    QUALITY STANDARDS:
                    - Commercial e-commerce photography grade
                    - Suitable for high-end fashion marketing
                    - Perfect garment representation without any distortion
                    - Natural, professional model positioning
                    - Clean, professional studio aesthetic
                    - Consistent visual style for series continuity
    
                    Ensure perfect visual consistency across all elements while maintaining natural, realistic appearance and professional fashion photography standards.          
                '''
            else:
                if generated_first_image_path and unique_num==1:
                    with open(generated_first_image_path, "rb") as f:
                        generated_first_image_path_image_data = f.read()
                    parts.append(types.Part.from_bytes(
                        mime_type="image/png",
                        data=generated_first_image_path_image_data,
                    ))
                image_prompt = f'''
                    Use exact same background and model face as uploaded model image and need to change only pose
                    
                    POSE SPECIFICATIONS (EXACT REPLICATION REQUIRED):
                    {pose_detail}
                    
                    GARMENT REQUIREMENTS:
                    - CRITICAL: Exact replication of reference garment required
                    - Match all design elements with 100% accuracy:
                      * Fabric texture and weave pattern
                      * Color saturation and tone precision
                      * Pattern details and placement
                      * Garment construction and seaming
                      * Style elements and embellishments
                      * Fit characteristics: Regular fit silhouette
                    - NO creative interpretation or modifications allowed
                    - Don't add any design or modifications in garment by your self
                    - Maintain authentic draping and fabric behavior
          
                    TECHNICAL SPECIFICATIONS:
                    - Ultra-high resolution (4K+), photorealistic quality
                    - Professional fashion photography lighting with soft shadows
                    - Precise fabric texture rendering and authentic draping for both pieces
                    - Color-accurate reproduction matching all reference materials
                    - Sharp focus on model and both garments with depth of field
                    - Professional model positioning and natural body language
                    - Seamless integration of all reference elements

                    QUALITY STANDARDS:
                    - Commercial e-commerce photography grade
                    - Suitable for high-end fashion marketing
                    - Perfect garment representation without any distortion
                    - Natural, professional model positioning
                    - Clean, professional studio aesthetic
                    - Consistent visual style for series continuity

                    Ensure perfect visual consistency across all elements while maintaining natural, realistic appearance and professional fashion photography standards.          
                '''

            parts.append(types.Part.from_text(text=image_prompt))

            pose_contents = [
                types.Content(
                    role="user",
                    parts=parts,
                ),
            ]

            response = client.models.generate_content(
                model=model_gemini,
                contents=pose_contents,
                config=generate_content_config
            )

            for part in response.candidates[0].content.parts:
                if part.text is not None:
                    print(part.text)
                elif part.inline_data is not None:
                    image = Image.open(BytesIO(part.inline_data.data))
                    output_filename = f"{uuid.uuid4()}_photoshoot_{unique_num + 1}.png"
                    base_image_filename = f"static/photoshoots_folders/{photoshoot_id}/{output_filename}"
                    image.save(base_image_filename)
                    upscaled_filename = f"static/photoshoots_folders/{photoshoot_id}/upscaled_{output_filename}"
                    response_upscale = upscale_image(base_image_filename, upscaled_filename)
                    if response_upscale:
                        all_generated_images.append("upscaled_" + output_filename)
                    else:
                        all_generated_images.append(output_filename)

                    if unique_num==0:
                        generated_first_image_path=base_image_filename
                        parts.pop()
                        parts.pop()
                    else:
                        parts.pop()

        total_credit = len(all_generated_images)
        cost_estimate = calculate_estimated_cost(
            num_poses=len(body_poses),
            has_upper_garment=bool(upper_garment_filename),
            has_lower_garment=bool(lower_garment_filename)
        )
        print(f"Estimated total cost: ${cost_estimate['estimated_total_cost']}")

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
