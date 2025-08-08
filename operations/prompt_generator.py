def generate_fashion_prompt(
        garment_category,
        user_params,
        background_description="Clean, minimalist studio background with soft lighting"
):
    """
    Generate optimized AI prompts for fashion photoshoots based on garment category and user parameters.

    Args:
        garment_category: One of ['upper_only', 'lower_only', 'one_piece_dress', 'full_body_separate', 'full_body_dress']
        user_params: Dictionary containing user selections from the form
        background_description: Background setting for the photoshoot

    Returns:
        Optimized prompt string for AI image generation
    """

    # Extract user parameters
    age_group = user_params.get('age_group', 'young-adult')
    gender = user_params.get('gender', 'female')
    ethnicity = user_params.get('ethnicity', 'indian')
    height = user_params.get('height', 'average')
    weight = user_params.get('weight', 'average')
    fitting = user_params.get('fitting', 'Regular Fit')
    age = user_params.get('age', '25')
    upper_garment_type = user_params.get('upper_garment_type', '')
    lower_garment_type = user_params.get('lower_garment_type', '')
    body_pose = user_params.get('pose', 'Full-body Front')

    # Create model description
    model_description = f"{age}-year-old {ethnicity} {gender} with {height} height and {weight} build"

    # Define garment category prompts
    prompts = {
        'upper_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified upper garment.

CRITICAL REQUIREMENTS:
1. FACE: Use the EXACT face from the reference face image - preserve all facial features, expressions, skin tone, and characteristics with 100% accuracy
2. UPPER GARMENT: Replicate the EXACT upper garment ({upper_garment_type}) from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, sleeve partially folded upward and garment construction identically
3. LOWER GARMENT: Wear complementary {lower_garment_type} that harmonizes with the upper garment - coordinate colors, maintain style consistency, ensure appropriate fit and length
4. POSE: {body_pose} with natural, confident posture
5. BACKGROUND: {background_description}
6. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping
- Color-accurate reproduction matching reference materials
- Sharp focus on model and garments with depth of field
- Professional model positioning and natural body language
- Seamless integration of all reference elements

Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'lower_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified lower garment.

CRITICAL REQUIREMENTS:
1. FACE: Use the EXACT face from the reference face image - preserve all facial features, expressions, skin tone, and characteristics with 100% accuracy
2. LOWER GARMENT: Replicate the EXACT lower garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements and garment construction identically
3. UPPER GARMENT: Wear any upper garment related to lower garment
4. POSE: {body_pose} with natural, confident posture
5. BACKGROUND: {background_description}
6. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Exact match if we have elastic waistband then please focus on exact elastic waistband fit and cut waistband details
- Clearly shows: if we have metal hook-and-bar in closure waistband then only show metal hook-and-bar with exact match
- Clearly shows: if we have the button and pocket then exact match Button detailing, Pocket placement and size 
- Precise fabric texture rendering and authentic draping
- Color-accurate reproduction matching reference materials
- Sharp focus on model and garments with depth of field
- Professional model positioning and natural body language
- Seamless integration of all reference elements

Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'one_piece_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified one-piece dress or garment.

CRITICAL REQUIREMENTS:
1. FACE: Use the EXACT face from the reference face image - preserve all facial features, expressions, skin tone, and characteristics with 100% accuracy
2. ONE-PIECE GARMENT: Replicate the EXACT dress/one-piece from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, neckline, hemline, and garment construction identically
3. COVERAGE ADAPTATION: 
   - If dress is full-length: Wear as standalone piece with appropriate undergarments
   - If dress is above-knee/short: Add complementary lower garment (leggings, tights, or appropriate bottom wear) that enhances the dress style
4. POSE: {body_pose} with natural, confident posture showcasing the garment's design
5. BACKGROUND: {background_description}
6. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping
- Color-accurate reproduction matching reference materials
- Sharp focus on model and garments with depth of field
- Professional model positioning and natural body language
- Accurate garment length and silhouette representation

Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'full_body_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified complete outfit with separate upper and lower garments.

CRITICAL REQUIREMENTS:
1. FACE: Use the EXACT face from the reference face image - preserve all facial features, expressions, skin tone, and characteristics with 100% accuracy
2. UPPER GARMENT: Replicate the EXACT upper garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, and garment construction identically
3. LOWER GARMENT: Replicate the EXACT lower garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, and garment construction identically
4. OUTFIT COORDINATION: Ensure both garments work harmoniously together while maintaining their individual reference accuracy
5. POSE: {body_pose} with natural, confident posture showcasing the complete outfit
6. BACKGROUND: {background_description}
7. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping for both pieces
- Color-accurate reproduction matching all reference materials
- Sharp focus on model and both garments with depth of field
- Professional model positioning and natural body language
- Seamless integration of all reference elements

Ensure perfect visual consistency across all elements while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'full_body_dress_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified complete dress outfit with additional garments.

CRITICAL REQUIREMENTS:
1. FACE: Use the EXACT face from the reference face image - preserve all facial features, expressions, skin tone, and characteristics with 100% accuracy
2. MAIN DRESS: Replicate the EXACT dress from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, and garment construction identically
3. ADDITIONAL GARMENTS: Replicate the EXACT additional pieces (leggings, jacket, accessories, etc.) from reference images - match all details precisely including fabric, color, pattern, and fit
4. LAYERED STYLING: Ensure all garment layers work together cohesively while maintaining individual reference accuracy
5. POSE: {body_pose} with natural, confident posture showcasing the complete layered ensemble
6. BACKGROUND: {background_description}
7. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping for all layers
- Color-accurate reproduction matching all reference materials
- Sharp focus on model and all garment layers with depth of field
- Professional model positioning and natural body language
- Accurate representation of garment layering and styling

Ensure perfect visual consistency across all elements while maintaining natural, realistic appearance and professional fashion photography standards.
"""
    }

    return prompts.get(garment_category, prompts['upper_garment'])

def single_generate_fashion_prompt(
        garment_category,
        user_params,
        background_description="Clean, minimalist studio background with soft lighting"
):
    """
    Generate optimized AI prompts for fashion photoshoots based on garment category and user parameters.

    Args:
        garment_category: One of ['upper_only', 'lower_only', 'one_piece_dress', 'full_body_separate', 'full_body_dress']
        user_params: Dictionary containing user selections from the form
        background_description: Background setting for the photoshoot

    Returns:
        Optimized prompt string for AI image generation
    """

    # Extract user parameters
    age_group = user_params.get('age_group', 'young-adult')
    gender = user_params.get('gender', 'female')
    ethnicity = user_params.get('ethnicity', 'indian')
    height = user_params.get('height', 'average')
    weight = user_params.get('weight', 'average')
    fitting = user_params.get('fitting', 'Regular Fit')
    age = user_params.get('age', '25')
    upper_garment_type = user_params.get('upper_garment_type', '')
    lower_garment_type = user_params.get('lower_garment_type', '')
    body_pose = user_params.get('pose', 'Full-body Front')

    # Create model description
    model_description = f"{age}-year-old {ethnicity} {gender} with {height} height and {weight} build"

    # Define garment category prompts
    prompts = {
        'upper_garment': f"""
Could you please create a model photoshoot for this upper garment

Replicate the EXACT upper garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, Clearly shows: Button detailing and garment construction identically

Human model age: {age} years ({ethnicity})
background: {background_description}
pose: {body_pose} with natural, confident posture
upper garment type: {upper_garment_type}
GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- If upper garment is formal shirt then only wearing a shirt tucked into pants or a skirt.
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping
- Color-accurate reproduction matching reference materials
- Sharp focus on model and garments with depth of field
- Professional model positioning and natural body language
- Seamless integration of all reference elements

Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'lower_garment': f"""
Could you please create a model photoshoot for this upper garment

Replicate the EXACT lower garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements and garment construction identically

Human model age: {age} years ({ethnicity})
background: {background_description}
pose: {body_pose} with natural, confident posture
lower garment type: {lower_garment_type}
GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Exact match if we have elastic waistband then please focus on exact elastic waistband fit and cut waistband details
- Clearly shows: if we have metal hook-and-bar in closure waistband then only show metal hook-and-bar with exact match
- Clearly shows: if we have the button and pocket then exact match Button detailing, Pocket placement and size 
- Precise fabric texture rendering and authentic draping
- Color-accurate reproduction matching reference materials
- Sharp focus on model and garments with depth of field
- Professional model positioning and natural body language
- Seamless integration of all reference elements

Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'one_piece_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified one-piece dress or garment.

CRITICAL REQUIREMENTS:
1. ONE-PIECE GARMENT: Replicate the EXACT dress/one-piece from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, neckline, hemline, and garment construction identically
2. COVERAGE ADAPTATION: 
   - If dress is full-length: Wear as standalone piece with appropriate undergarments
   - If dress is above-knee/short: Add complementary lower garment (leggings, tights, or appropriate bottom wear) that enhances the dress style
3. POSE: {body_pose} with natural, confident posture showcasing the garment's design
4. BACKGROUND: {background_description}
5. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping
- Color-accurate reproduction matching reference materials
- Sharp focus on model and garments with depth of field
- Professional model positioning and natural body language
- Accurate garment length and silhouette representation

Ensure perfect visual consistency while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'full_body_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified complete outfit with separate upper and lower garments.

CRITICAL REQUIREMENTS:
1. UPPER GARMENT: Replicate the EXACT upper garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, and garment construction identically
2. LOWER GARMENT: Replicate the EXACT lower garment from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, and garment construction identically
3. OUTFIT COORDINATION: Ensure both garments work harmoniously together while maintaining their individual reference accuracy
4. POSE: {body_pose} with natural, confident posture showcasing the complete outfit
5. BACKGROUND: {background_description}
6. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping for both pieces
- Color-accurate reproduction matching all reference materials
- Sharp focus on model and both garments with depth of field
- Professional model positioning and natural body language
- Seamless integration of all reference elements

Ensure perfect visual consistency across all elements while maintaining natural, realistic appearance and professional fashion photography standards.
""",

        'full_body_dress_garment': f"""
Create a professional fashion photoshoot image of a {model_description} wearing the specified complete dress outfit with additional garments.

CRITICAL REQUIREMENTS:
1. MAIN DRESS: Replicate the EXACT dress from reference image - match fabric texture, color saturation, pattern details, fit precision, style elements, and garment construction identically
2. ADDITIONAL GARMENTS: Replicate the EXACT additional pieces (leggings, jacket, accessories, etc.) from reference images - match all details precisely including fabric, color, pattern, and fit
3. LAYERED STYLING: Ensure all garment layers work together cohesively while maintaining individual reference accuracy
4. POSE: {body_pose} with natural, confident posture showcasing the complete layered ensemble
5. BACKGROUND: {background_description}
6. GARMENT FITTING: {fitting}

TECHNICAL SPECIFICATIONS:
- Ultra-high resolution (4K+), photorealistic quality
- Professional fashion photography lighting with soft shadows
- Precise fabric texture rendering and authentic draping for all layers
- Color-accurate reproduction matching all reference materials
- Sharp focus on model and all garment layers with depth of field
- Professional model positioning and natural body language
- Accurate representation of garment layering and styling

Ensure perfect visual consistency across all elements while maintaining natural, realistic appearance and professional fashion photography standards.
"""
    }

    return prompts.get(garment_category, prompts['upper_garment'])

