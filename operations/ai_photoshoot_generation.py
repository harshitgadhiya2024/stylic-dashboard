import base64
import random
import uuid

from flask import url_for, session
from openai import OpenAI
import os
from PIL import Image

from operations.mail_sending import emailOperation
from operations.mongo_operation import mongoOperation
from operations.prompt_generator import generate_fashion_prompt
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
            prompt_parts.append(f"Professional headshot portrait of a {params['age']} years of {params['gender']} person")

            # Face structure
            face_desc = f"{params['facial_structure']['face_shape']} face with {params['facial_structure']['jawline']} jawline and {params['facial_structure']['cheekbones']} cheekbones"
            prompt_parts.append(face_desc)

            # Eyes
            eye_desc = f"{params['eyes']['size']} {params['eyes']['shape']} {params['eyes']['color']} eyes with {params['eyes']['eyebrows']} eyebrows"
            prompt_parts.append(eye_desc)

            # Nose and mouth
            prompt_parts.append(f"{params['nose']['size']} {params['nose']['shape']} nose")
            prompt_parts.append(f"{params['mouth']['lips']} {params['mouth']['shape']} lips")

            # Hair
            hair_desc = f"{params['hair']['length']} {params['hair']['texture']} {params['hair']['color']} hair styled {params['hair']['style']}"
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

        all_generated_images = []

        # Face parameters for consistent generation
        face_params = {
            "facial_structure": {
                "face_shape": random.choice(["oval", "round", "square", "heart-shaped", "diamond", "oblong"]),
                "jawline": "soft",
                "cheekbones": random.choice(["subtle", "moderate", "prominent", "high"])
            },
            "eyes": {
                "shape": random.choice(["almond", "round", "hooded", "deep-set", "upturned", "downturned"]),
                "color": "dark brown",
                "size": random.choice(["small", "medium", "large"]),
                "eyebrows": random.choice(["thin", "medium", "thick", "arched", "straight", "bushy"])
            },
            "nose": {
                "shape": random.choice(["straight", "button", "roman", "aquiline", "snub", "broad"]),
                "size": "small"
            },
            "mouth": {
                "lips": "thin",
                "shape": "straight"
            },
            "hair": {
                "color": random.choice(["black", "dark brown", "brown"]),
                "texture": random.choice(["straight", "wavy", "curly", "coily"]),
                "length": random.choice(["short", "medium", "long"]),
                "style": random.choice(["loose", "ponytail", "bun", "braided", "tousled", "sleek"])
            },
            "skin": {
                "tone": random.choice(["light", "medium", "olive"]),
                "texture": "smooth"
            },
            "age_group": garment_mapping_dict.get("age_group"),
            "age": garment_mapping_dict.get("age"),
            "gender": garment_mapping_dict.get("gender"),
            "expression": random.choice(["neutral", "slight smile", "warm smile", "confident"]),
            "lighting": random.choice(["soft natural light", "dramatic lighting", "golden hour", "studio lighting", "side lighting"])
        }

        # Generate face
        photo_file_name = f"{uuid.uuid4()}generatedface.png"
        face_photo_url = generator.generate_model_face(face_params, photo_file_name, photoshoot_id)

        # Fix the logic issue with face generation loop
        while not face_photo_url:  # Changed from "while face_photo_url:" which was incorrect
            face_photo_url = generator.generate_model_face(face_params, photo_file_name, photoshoot_id)

        mongoOperation().update_mongo_data(
            "photoshoot_data",
            {"id": user_id, "photoshoot_id": photoshoot_id},
            {"status": "model_face_generated"}
        )

        all_generated_images.append(photo_file_name)

        upper_garment_image = upper_garment_filename
        below_garment_image = lower_garment_filename
        upper_garment_category = garment_mapping_dict.get("upper_garment_type")
        below_garment_category = garment_mapping_dict.get("lower_garment_type")
        garment_type = garment_mapping_dict.get("upload_garment_type")

        poses = garment_mapping_dict.get("selected_poses", [])

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
            "Model gazing over sunglasses, strong jawline highlighted, glossy backdrop"
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
                'age': age,
                'upper_garment_type': upper_garment_category,
                'lower_garment_type': below_garment_category,
                'pose': body_pose
            }

            image_prompt = generate_fashion_prompt(garment_type, sample_params)

            output_filename = f"{uuid.uuid4()}_photoshoot_{num + 1}.png"
            result = generator.generate_photoshoot_image(
                photoshoot_id, image_prompt, face_photo_url, garment_type, upper_garment_image, below_garment_image,
                output_filename
            )

            if result:
                all_generated_images.append(output_filename)
                print(f"Successfully generated: {result}")
            else:
                print(f"Failed to generate image for pose: {body_pose}")

        if len(all_generated_images)<2:
            html_format = htmlOperation().photoshoot_faileur(photoshoot_id)
            emailOperation().send_email("info.stylicai@gmail.com", "Stylic: Your Reset Password Link", html_format)
            return {
                'status': 'failed',
                'total_images': len(all_generated_images),
                'total_credit': 0,
                'all_images': garment_mapping_dict.get("all_images", [])
            }

        total_credit = len(all_generated_images) - 1
        user_id = garment_mapping_dict.get("id")
        user_data = list(mongoOperation().get_spec_data_from_coll("company_data", {"id": user_id}))

        if user_data:
            user_credit = int(user_data[0]["credit"])
            remaining_credit = user_credit - total_credit
            mongoOperation().update_mongo_data("company_data", {"id": user_id}, {"credit": remaining_credit})

        all_images = garment_mapping_dict.get("all_images", [])
        for images in all_generated_images:
            garment_image_url = url_for('static',
                                              filename=f'photoshoots_folders/{photoshoot_id}/{images}',
                                              _external=True)
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
