import time
import os
from openai import OpenAI
import base64

from utils.constant import constant_dict

# Create output directory
output_dir = "generated_poses"
os.makedirs(output_dir, exist_ok=True)

# Your 30 pose prompts
fashion_poses = [
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
    'Complete pose - Model standing on one leg with other bent, playful posture showing full outfit against vibrant colored backdrop']

for i, prompt in enumerate(fashion_poses, start=30):
    print(f"Generating realistic human model image for pose {i}...")
    try:
        prompt = f"Generating realistic human model image for pose {prompt}"
        client = OpenAI(
            api_key=constant_dict.get("openai_key"))

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt
        )

        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)

        # Save the image to a file
        with open(f"generated_poses/pose_new_{i}.png", "wb") as f:
            f.write(image_bytes)
        print(f"✅ Saved: generated_poses/pose_new_{i}.png")
    except Exception as e:
        print(f"❌ Error on pose {i}: {e}")

    # Optional: avoid rate limits
    time.sleep(2)
