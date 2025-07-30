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


mapping_dict = {}
for num, var in enumerate(fashion_poses):
    mapping_dict[f"pose_{num}"] = var

print(mapping_dict)