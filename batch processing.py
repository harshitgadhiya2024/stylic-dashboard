import os
import random
import subprocess
import uuid
from concurrent.futures import ProcessPoolExecutor

from PIL import Image
from io import BytesIO
from google import genai
from google.genai import types

pose_data_mapping = {
    "front": [
        "half upper body front view: Professional headshot, model standing straight with arms relaxed at sides, direct eye contact with camera, neutral confident expression, studio lighting",
        "half upper body front view: Model with both hands placed firmly on hips, shoulders back, confident stance, upper body from waist up, front facing camera",
        "half upper body front view: Arms folded across chest, relaxed but assertive posture, model looking directly at camera, professional portrait style",
        "half upper body front view: Single hand resting on hip, other arm hanging naturally at side, casual confident pose, front view upper body shot",
        "half upper body front view: Both palms pressed together at chest level in prayer position, centered pose, serene expression, front facing",
        "half upper body front view: Both hands forming rectangular frame around face, elbows out, creative portrait pose, engaging eye contact",
        "half upper body front view: One hand gently cupping chin with elbow supported, thoughtful contemplative expression, intimate portrait style",
        "half upper body front view: Both hands showing peace sign gesture near face level, playful energetic pose, bright expression",
        "half upper body front view: Both thumbs up with fists closed, enthusiastic energetic pose, confident smile, motivational portrait",
        "half upper body front view: One hand running through or touching hair naturally, casual relaxed movement, soft expression",
        "half upper body front view: Model wearing sunglasses, arms at sides, cool confident demeanor, front facing portrait",
        "half upper body front view: Wearing baseball cap or beanie, one hand adjusting the brim, casual street style portrait",
        "half upper body front view: Headphones draped around neck, hands relaxed, modern lifestyle portrait, front view",
        "half upper body front view: One arm raised checking wristwatch, other hand at side, professional business style pose",
        "half upper body front view: Holding smartphone at chest level while looking at camera, modern contemporary portrait",
        "half upper body front view: Model sitting on chair leaning slightly forward, elbows resting on knees, engaged expression",
        "half upper body front view: Sitting upright in chair with arms crossed, confident professional posture, direct gaze",
        "half upper body front view: Sitting with one elbow resting on chair arm, relaxed comfortable pose, natural expression",
        "half upper body front view: Sitting on high stool with hands resting on thighs, casual contemporary pose, front facing",
        "half upper body front view: Mid-shoulder shrug gesture with raised shoulders and palms facing up, expressive animated face",
        "half upper body front view: Both hands clasped behind back, chest open, military-style confident posture, straight spine",
        "half upper body front view: One hand touching collarbone gently, other arm relaxed, elegant feminine pose, soft lighting",
        "half upper body front view: Both arms stretched wide in welcoming gesture, open body language, warm inviting expression",
        "half upper body front view: Finger pointing directly at camera, engaging interactive pose, playful or assertive expression",
        "half upper body front view: Both hands forming heart shape at chest level, romantic or playful gesture, sweet expression",
        "half upper body front view: One hand covering one eye playfully, other hand at side, peek-a-boo style portrait",
        "half upper body front view: Both hands gently holding sides of face, dreamy contemplative expression, intimate portrait",
        "half upper body front view: Arms stretched overhead in victory or celebration pose, triumphant joyful expression",
        "half upper body front view: One hand making 'shh' gesture with finger to lips, mysterious secretive expression",
        "half upper body front view: Both hands interlocked fingers stretched forward, casual relaxed stretch pose",
        "half upper body front view: One hand saluting, military or respectful gesture, disciplined confident posture",
        "half upper body front view: Both hands on chest expressing gratitude or sincerity, heartfelt emotional expression",
        "half upper body front view: One hand waving hello or goodbye, friendly approachable gesture, welcoming smile",
        "half upper body front view: Both fists clenched in determined or fighting stance, strong powerful expression",
        "half upper body front view: One hand adjusting collar or tie, professional grooming gesture, business portrait style",
        "half upper body front view: Both hands holding imaginary steering wheel, playful driving pose, animated expression",
        "half upper body front view: One hand making rock and roll horn sign, rebellious or musical gesture, edgy expression",
        "half upper body front view: Both hands pressed against invisible wall, mime-like theatrical pose, concentrated expression",
        "half upper body front view: One hand making OK sign, other relaxed, positive affirmative gesture, satisfied expression",
        "half upper body front view: Both hands in defensive blocking position, protective or martial arts inspired pose",
        "half upper body front view: One hand making gun gesture pointed upward, playful or cowboy-style pose, confident smirk",
        "half upper body front view: Both hands forming binoculars around eyes, searching or exploring gesture, curious expression",
        "half upper body front view: One hand making chef's kiss gesture, appreciative or perfect gesture, satisfied expression",
        "half upper body front view: Both arms hugging self in self-embrace, comforting or cold gesture, cozy expression",
        "half upper body front view: One hand making call-me phone gesture, casual social interaction pose, friendly expression",
        "half upper body front view: Both hands in jazz hands position, theatrical energetic pose, show-business expression",
        "half upper body front view: One hand making thumbs down gesture, disapproving or negative feedback pose, critical expression",
        "half upper body front view: Both hands in time-out T formation, referee or break gesture, authoritative expression",
        "half upper body front view: One hand covering mouth in surprise, other at side, shocked or amazed expression",
        "half upper body front view: Both hands making quotation marks gesture, emphasizing or ironic pose, knowing expression",
        "half upper body front view: One hand making money gesture rubbing fingers, materialistic or expensive pose, sly expression",
        "half upper body front view: Both hands in namaste prayer position at heart, spiritual or respectful pose, peaceful expression",
        "half upper body front view: One hand making stop gesture palm forward, commanding or halt pose, serious expression",
        "half upper body front view: Both hands counting numbers on fingers, mathematical or listing pose, concentrated expression",
        "half upper body front view: One hand making L-shape on forehead, loser gesture, self-deprecating or playful expression",
        "half upper body front view: Both hands in applauding position, appreciative or celebratory pose, pleased expression",
        "half upper body front view: One hand making pinching gesture, small or precise measurement pose, focused expression",
        "half upper body front view: Both hands forming W shape for win, victorious or team spirit pose, triumphant expression",
        "half upper body front view: One hand making thinking gesture with finger on temple, contemplative pose, pensive expression",
        "half upper body front view: Both hands in prayer position raised above head, grateful or blessed pose, reverent expression",
        "half upper body front view: One hand making come-here beckoning gesture, inviting or seductive pose, alluring expression"
    ],

    "side": [
        "half side angle upper body: Perfect side profile, model standing with arms at sides, looking straight ahead, clean silhouette",
        "half side angle upper body: Side stance with head turned to look over shoulder toward camera, dramatic portrait angle",
        "half side angle upper body: Standing sideways with arms folded across chest, strong profile silhouette, confident posture",
        "half side angle upper body: Side view with near hand on hip, far arm hanging naturally, elegant side profile",
        "half side angle upper body: Side stance with both hands placed on hips, confident professional posture, clear silhouette",
        "half side angle upper body: Side profile with one or both arms extended forward in reaching motion, dynamic movement",
        "half side angle upper body: Side view with one arm raised high above head, stretching upward, graceful elongated pose",
        "half side angle upper body: Side profile with hands clasped behind head and elbows out, relaxed confident pose",
        "half side angle upper body: Leaning to one side with arm extended, creating curved artistic silhouette, fluid movement",
        "half side angle upper body: Mid-motion hair flip captured from side angle, dynamic natural movement, expressive pose",
        "half side angle upper body: Side profile wearing sunglasses, looking straight ahead, cool professional demeanor",
        "half side angle upper body: Side view adjusting hat brim or tipping hat, casual greeting gesture, natural movement",
        "half side angle upper body: Side profile holding phone to ear in conversation pose, natural lifestyle shot",
        "half side angle upper body: Side angle wearing headphones with hands adjusting them, contemporary lifestyle portrait",
        "half side angle upper body: Side profile checking watch on raised wrist, professional business style pose",
        "half side angle upper body: Sitting on chair viewed from side, hands on knees or thighs, relaxed natural pose",
        "half side angle upper body: Sitting sideways on chair leaning forward or backward, casual comfortable position",
        "half side angle upper body: Side profile sitting on high stool with feet positioned naturally, contemporary pose",
        "half side angle upper body: Sitting with elbow resting on chair arm, side angle view, relaxed professional pose",
        "half side angle upper body: Side view with animated hand gesture, mid-conversation pose, expressive natural movement",
        "half side angle upper body: Side profile with near arm across waist, far arm raised to touch face gently, contemplative pose",
        "half side angle upper body: Side stance with both arms stretched forward in pushing motion, dynamic action silhouette",
        "half side angle upper body: Side view with near hand covering mouth in whisper gesture, secretive intimate pose",
        "half side angle upper body: Side profile with one arm bent drinking from cup or bottle, natural lifestyle moment",
        "half side angle upper body: Side angle with both hands pressed together in prayer position, spiritual meditative pose",
        "half side angle upper body: Side view with near arm raised in saluting gesture, respectful military-style pose",
        "half side angle upper body: Side profile with hand running through hair from back to front, sensual grooming gesture",
        "half side angle upper body: Side stance with both arms hugging self, comforting or cold protective gesture",
        "half side angle upper body: Side view with near hand shading eyes looking into distance, searching explorer pose",
        "half side angle upper body: Side profile with one arm extended pointing forward, directing or indicating gesture",
        "half side angle upper body: Side angle with both hands on chest in gratitude or surprise expression, emotional pose",
        "half side angle upper body: Side view with near arm raised making peace sign, playful optimistic gesture",
        "half side angle upper body: Side profile with hand cupping ear in listening gesture, attentive focused pose",
        "half side angle upper body: Side stance with both arms raised in victory celebration, triumphant joyful silhouette",
        "half side angle upper body: Side view with near hand making thumbs up gesture, positive approval pose",
        "half side angle upper body: Side profile with arm bent adjusting collar or necklace, grooming refinement gesture",
        "half side angle upper body: Side angle with both hands forming heart shape, romantic loving gesture silhouette",
        "half side angle upper body: Side view with near arm extended in stop gesture palm forward, commanding authoritative pose",
        "half side angle upper body: Side profile with hand making call-me phone gesture, casual social interaction pose",
        "half side angle upper body: Side stance with both arms crossed behind back, formal disciplined military posture",
        "half side angle upper body: Side view with near hand touching temple in thinking gesture, intellectual contemplative pose",
        "half side angle upper body: Side profile with arm raised checking bicep muscle, fitness strength demonstration pose",
        "half side angle upper body: Side angle with both hands clapping together, appreciative celebratory gesture",
        "half side angle upper body: Side view with near arm making rock and roll horn sign, rebellious music gesture",
        "half side angle upper body: Side profile with hand covering one eye in playful peek-a-boo gesture, whimsical pose",
        "half side angle upper body: Side stance with both arms stretched wide in welcoming embrace gesture, open inviting pose",
        "half side angle upper body: Side view with near hand making OK sign, positive confirmation gesture, satisfied expression",
        "half side angle upper body: Side profile with arm raised in fist pump celebration, energetic victorious pose",
        "half side angle upper body: Side angle with both hands pressed against invisible wall, mime theatrical performance pose",
        "half side angle upper body: Side view with near hand making shh gesture finger to lips, mysterious secretive pose",
        "half side angle upper body: Side profile with arm extended holding imaginary microphone, performance singing pose",
        "half side angle upper body: Side stance with both hands forming binoculars around eyes, searching exploring gesture",
        "half side angle upper body: Side view with near arm raised in defensive blocking position, protective martial arts pose",
        "half side angle upper body: Side profile with hand making chef's kiss gesture, appreciative perfection expression",
        "half side angle upper body: Side angle with both arms in jazz hands position, theatrical energetic performance pose",
        "half side angle upper body: Side view with near hand making gun gesture, playful cowboy or action pose",
        "half side angle upper body: Side profile with arm raised waving goodbye or hello, friendly social gesture",
        "half side angle upper body: Side stance with both hands interlocked stretching forward, casual relaxation pose",
        "half side angle upper body: Side view with near hand making L-shape on forehead, self-deprecating playful gesture",
        "half side angle upper body: Side profile with arm bent in flexing muscle pose, strength fitness demonstration",
        "half side angle upper body: Side angle with both hands covering face in embarrassment or surprise, emotional reaction pose"
    ],

    "zoomed": [
        "zoomed detail view: Extreme close-up with both hands gently framing the face, fingers visible, intimate portrait",
        "zoomed detail view: Close-up with one hand resting on cheek with palm visible, soft intimate expression",
        "zoomed detail view: Tight shot of fingers running through hair strands, artistic detailed capture",
        "zoomed detail view: Artistic close-up with hand partially covering one eye, mysterious peek-a-boo effect",
        "zoomed detail view: Detailed shot of hands pressed together in prayer position, serene contemplative mood",
        "zoomed detail view: Extreme close-up centering on the eyes and upper face area, intense eye contact",
        "zoomed detail view: Close-up profile focusing on eye looking sideways, dramatic side angle detail",
        "zoomed detail view: Detailed shot capturing wink expression, playful intimate close-up",
        "zoomed detail view: Close-up emphasizing raised eyebrow and forehead expression, curious engaged look",
        "zoomed detail view: Detail shot focusing on eyes behind sunglasses, mysterious cool expression",
        "zoomed detail view: Close-up of index finger pointing toward camera, direct engaging gesture",
        "zoomed detail view: Tight shot of hand making peace sign near face, playful energetic detail",
        "zoomed detail view: Detailed view of thumbs up gesture with hand in sharp focus, positive expression",
        "zoomed detail view: Close-up of finger pressed against lips in shush gesture, mysterious intimate pose",
        "zoomed detail view: Detail shot of hands with fingers interlocked together, artistic hand composition",
        "zoomed detail view: Close-up of wrist and watch with hand positioned to show timepiece, luxury detail",
        "zoomed detail view: Tight shot emphasizing rings on fingers with hand elegantly posed, jewelry focus",
        "zoomed detail view: Close-up of ear with earphone, side profile detail, modern lifestyle shot",
        "zoomed detail view: Detail shot showing face partially shadowed by hat brim, dramatic lighting effect",
        "zoomed detail view: Close-up focusing on neck and collar area with hand adjusting, refined detail shot",
        "zoomed detail view: Extreme close-up of single eye with detailed eyelashes and iris, macro portrait focus",
        "zoomed detail view: Tight shot of lips with finger touching corner of mouth, sensual detailed expression",
        "zoomed detail view: Close-up of hand making heart shape with thumb and forefinger, romantic gesture detail",
        "zoomed detail view: Detail shot of fingertips touching temple in thinking pose, intellectual contemplation focus",
        "zoomed detail view: Close-up of hand cupping chin with visible fingertip details, thoughtful intimate pose",
        "zoomed detail view: Tight shot of knuckles and closed fist, strength and determination detail focus",
        "zoomed detail view: Extreme close-up of eyebrow area with hand brushing through brow, grooming gesture detail",
        "zoomed detail view: Detail shot of palm facing camera in stop gesture, commanding hand focus",
        "zoomed detail view: Close-up of fingers making OK sign with sharp detail on hand positioning",
        "zoomed detail view: Tight shot of hand making rock and roll horns near ear, rebellious gesture detail",
        "zoomed detail view: Detail view of fingers forming gun shape pointing upward, playful hand gesture focus",
        "zoomed detail view: Close-up of hand making call-me phone gesture with pinky and thumb extended",
        "zoomed detail view: Extreme close-up of nostril and nose bridge area, artistic facial detail study",
        "zoomed detail view: Tight shot of earlobe and ear curve with earring detail, jewelry and anatomy focus",
        "zoomed detail view: Detail shot of cheekbone and temple area with dramatic side lighting shadows",
        "zoomed detail view: Close-up of dimple area when smiling, capturing facial expression detail",
        "zoomed detail view: Tight shot of forehead wrinkles during expression, character and emotion detail",
        "zoomed detail view: Detail view of neck and Adam's apple area, masculine anatomical focus",
        "zoomed detail view: Close-up of collarbone and shoulder transition with hand placement, elegant anatomy detail",
        "zoomed detail view: Extreme close-up of eyebrow hair texture and skin pores, macro beauty detail",
        "zoomed detail view: Tight shot of hand making thumbs down gesture with finger detail focus",
        "zoomed detail view: Detail view of fingers counting numbers one through five, educational hand gesture",
        "zoomed detail view: Close-up of hand making money gesture rubbing fingers, materialistic detail focus",
        "zoomed detail view: Tight shot of fingers making quotation marks in air, expressive gesture detail",
        "zoomed detail view: Detail view of hand making L-shape on forehead, self-deprecating gesture focus",
        "zoomed detail view: Close-up of fingers pinching together showing small measurement, precision gesture detail",
        "zoomed detail view: Extreme close-up of single tear on cheek, emotional dramatic detail",
        "zoomed detail view: Tight shot of mouth corner during subtle smile, micro-expression detail focus",
        "zoomed detail view: Detail view of hand making chef's kiss gesture with fingertips, appreciation focus",
        "zoomed detail view: Close-up of fingers forming W shape for win, victory gesture hand detail",
        "zoomed detail view: Tight shot of palm lines and hand creases, palmistry and character detail study",
        "zoomed detail view: Detail view of fingernails and cuticles with manicured hand, beauty care focus",
        "zoomed detail view: Close-up of knuckle dimples and hand bone structure, anatomical detail study",
        "zoomed detail view: Extreme close-up of skin texture on back of hand, dermatological detail focus",
        "zoomed detail view: Tight shot of thumb and forefinger making precise pinch, delicate gesture detail",
        "zoomed detail view: Detail view of wrist bone and tendon definition, anatomical structure focus",
        "zoomed detail view: Close-up of hand veins and vascular detail on back of hand, medical aesthetic focus",
        "zoomed detail view: Tight shot of finger joints and knuckle definition, hand anatomy detail study",
        "zoomed detail view: Detail view of palm heel and wrist transition area, hand structure focus",
        "zoomed detail view: Close-up of fingertip whorls and fingerprint patterns, forensic detail aesthetic",
        "zoomed detail view: Extreme close-up of hand freckles or beauty marks, skin characteristic detail focus"
    ],

    "full": [
        "full body: Standing with feet shoulder-width apart, hands on hips, confident power stance, full body front view",
        "full body: Classic runway pose with arms extended horizontally, one leg slightly forward, professional model stance",
        "full body: Leaning against invisible wall with one shoulder back, arms crossed, casual confident full body pose",
        "full body: Standing with weight on one leg, hip popped, opposite knee slightly bent, natural relaxed stance",
        "full body: Military-style straight posture with arms at sides, feet together, formal professional pose",
        "full body: Captured mid-step with one foot forward, natural walking motion, dynamic movement shot",
        "full body: Mid-jump with arms up and legs bent, energetic motion frozen in time, athletic pose",
        "full body: Arms out with one leg lifted, as if caught mid-spin, graceful dance-like movement",
        "full body: Full body stretch with arms reaching toward sky, standing on tiptoes, aspirational pose",
        "full body: One leg forward in lunge position, arms balanced for stability, strong athletic stance",
        "full body: Sitting upright on chair with feet flat on ground, hands on thighs, professional seated pose",
        "full body: Sitting cross-legged on ground with hands resting on knees, relaxed casual floor pose",
        "full body: Sitting on edge of surface with legs dangling, hands gripping edge, casual contemporary pose",
        "full body: Sitting on high stool leaning forward with elbows on knees, engaged conversational pose",
        "full body: Kneeling on one knee with other leg up, hands positioned naturally, dynamic grounded pose",
        "full body: Classic contrapposto pose with weight on one leg, opposite hip out, S-curve artistic silhouette",
        "full body: Arms positioned to create interesting geometric shapes and angles, artistic creative pose",
        "full body: Perfectly symmetrical pose with matching arm and leg positions, balanced formal stance",
        "full body: Intentionally unbalanced pose with contrasting arm positions, dynamic asymmetrical composition",
        "full body: Pose designed to create striking silhouette with dramatic arm and leg positioning, artistic shadow play",
        "full body: Standing with legs wide apart, arms crossed over chest, commanding authoritative stance",
        "full body: One foot up on elevated surface, hands on raised knee, explorer or hiker pose",
        "full body: Standing on one leg with other leg bent behind, arms out for balance, playful flamingo pose",
        "full body: Crouching down with hands on ground for support, athletic starting position or urban pose",
        "full body: Standing with arms spread wide in welcoming gesture, legs slightly apart, open inviting stance",
        "full body: Walking pose with opposite arm and leg forward, natural stride captured mid-motion",
        "full body: Sitting on ground with legs extended straight, leaning back on hands, relaxed beach pose",
        "full body: Standing sideways with head turned toward camera, profile body with front face view",
        "full body: Jumping with both arms raised in victory, legs spread wide, celebratory triumph pose",
        "full body: Standing with one hand shading eyes looking into distance, explorer or scout pose",
        "full body: Sitting in chair leaning back with arms behind head, relaxed confident executive pose",
        "full body: Standing with legs together, arms at sides, simple neutral full body reference pose",
        "full body: Lying on side propped up on elbow, legs extended, casual reclining ground pose",
        "full body: Standing with one leg crossed over the other, arms folded, patient waiting stance",
        "full body: Mid-stretch with arms overhead and back arched, morning wake-up or exercise pose",
        "full body: Sitting with knees drawn up to chest, arms wrapped around legs, contemplative huddle pose",
        "full body: Standing with weight shifted back, arms pushing forward, defensive or resistant stance",
        "full body: Walking up stairs pose with one foot elevated, hand on railing, ascending motion",
        "full body: Standing with arms akimbo, elbows out, hands on waist, confident superhero stance",
        "full body: Squatting position with hands on ground, athletic or breakdancing foundation pose",
        "full body: Standing with one arm raised pointing upward, inspirational or directing gesture pose",
        "full body: Sitting backwards on chair with arms draped over back, casual rebellious pose",
        "full body: Standing in doorway with hands on frame, leaning forward, casual conversation stance",
        "full body: Marching pose with one knee raised high, arms swinging naturally, military or parade step",
        "full body: Standing with feet together, hands clasped behind back, formal waiting or inspection pose",
        "full body: Reclining on ground with one knee up, arm behind head, relaxed outdoor leisure pose",
        "full body: Standing with legs spread, hands on knees, bent over stretching or tired pose",
        "full body: Jumping jack position with arms and legs spread wide, energetic exercise pose",
        "full body: Standing with one foot forward in fighting stance, fists raised, martial arts pose",
        "full body: Sitting Indian-style with perfect posture, hands in meditation position, zen pose",
        "full body: Standing with arms outstretched like airplane wings, legs together, playful flying pose",
        "full body: Kneeling with both knees down, sitting back on heels, formal respectful position",
        "full body: Standing with one hip out, hand on hip, other arm hanging loose, fashion model pose",
        "full body: Lying flat on back with arms and legs spread like starfish, relaxed sprawling pose",
        "full body: Standing with feet wide, arms reaching in opposite directions, dynamic stretching pose",
        "full body: Sitting on ground with legs in butterfly position, hands on ankles, yoga flexibility pose",
        "full body: Standing with one leg kicked back, arms forward for balance, dynamic kicking motion",
        "full body: Sitting at edge with legs crossed, chin resting on hand, thoughtful contemplative pose",
        "full body: Standing with arms crossed high on chest, legs slightly apart, defensive or cold pose",
        "full body: Mid-cartwheel with hands on ground, legs in air, athletic gymnastic movement pose",
        "full body: Standing with perfect posture, hands at sides, head high, formal presentation stance"
    ],

    "back": [
        "half Back view upper body: Model standing with back to camera, arms relaxed at sides, head straight forward, clean back silhouette",
        "half Back view upper body: Back view with both hands placed on hips, confident posture, shoulders back, strong stance",
        "half Back view upper body: Standing with back to camera, arms crossed behind, relaxed professional pose, head held high",
        "half Back view upper body: Back view with one hand on hip, other arm hanging naturally, casual confident positioning",
        "half Back view upper body: Model with back to camera, both arms raised above head in stretch, elegant extended pose",
        "half Back view upper body: Back view with hands clasped behind head, elbows out, relaxed contemplative stance",
        "half Back view upper body: Standing with back to camera, one hand running through hair, natural grooming gesture",
        "half Back view upper body: Back silhouette with arms extended to sides horizontally, creating T-shape, balanced pose",
        "half Back view upper body: Model with back to camera, hands behind back in formal at-ease position, professional stance",
        "half Back view upper body: Back view with one arm reaching across body to opposite shoulder, stretching motion",
        "half Back view upper body: Standing with back to camera wearing sunglasses, head turned slightly showing profile edge",
        "half Back view upper body: Back view adjusting hat or cap from behind, casual styling gesture, natural movement",
        "half Back view upper body: Model with back to camera, headphones visible around neck, modern lifestyle shot",
        "half Back view upper body: Back view checking watch on wrist, arm positioned to show timepiece from behind",
        "half Back view upper body: Standing with back to camera holding phone, engaged in conversation, contemporary pose",
        "half Back view upper body: Back view sitting on chair, hands resting on chair back, relaxed seated position",
        "half Back view upper body: Sitting with back to camera, one elbow resting on chair arm, casual comfortable pose",
        "half Back view upper body: Back view sitting on stool, feet positioned naturally, contemporary casual stance",
        "half Back view upper body: Model sitting with back to camera, both hands on knees, upright professional posture",
        "half Back view upper body: Back view with animated gesture, hands in motion, expressive body language from behind",
        "half Back view upper body: Standing with back to camera, both arms crossed over chest, defensive or contemplative stance",
        "half Back view upper body: Back view with one arm raised in pointing gesture, directing or indicating from behind",
        "half Back view upper body: Model with back to camera, hands pressed together in prayer position, spiritual pose",
        "half Back view upper body: Back view with both arms stretched forward in pushing motion, dynamic action silhouette",
        "half Back view upper body: Standing with back to camera, one hand covering back of neck, tired or stressed gesture",
        "half Back view upper body: Back view with both hands forming heart shape above head, romantic gesture from behind",
        "half Back view upper body: Model with back to camera, one arm raised making peace sign, optimistic gesture",
        "half Back view upper body: Back view with hands cupped around mouth as if shouting, calling gesture from behind",
        "half Back view upper body: Standing with back to camera, both arms raised in victory celebration, triumphant silhouette",
        "half Back view upper body: Back view with one hand shading eyes looking into distance, searching pose from behind",
        "half Back view upper body: Model with back to camera, arms wrapped around self in self-embrace, comforting gesture",
        "half Back view upper body: Back view with both hands on lower back, stretching or pain relief gesture",
        "half Back view upper body: Standing with back to camera, one arm making thumbs up gesture, positive approval from behind",
        "half Back view upper body: Back view with hands interlocked fingers stretching overhead, morning stretch pose",
        "half Back view upper body: Model with back to camera, one hand adjusting collar or neckline, grooming gesture",
        "half Back view upper body: Back view with both arms in defensive blocking position, protective martial arts stance",
        "half Back view upper body: Standing with back to camera, hands making rock and roll horns, rebellious gesture from behind",
        "half Back view upper body: Back view with one arm raised in saluting gesture, respectful military-style pose",
        "half Back view upper body: Model with back to camera, both hands clapping together, appreciative gesture from behind",
        "half Back view upper body: Back view with one hand making call-me phone gesture, social interaction from behind",
        "half Back view upper body: Standing with back to camera, arms in jazz hands position, theatrical performance pose",
        "half Back view upper body: Back view with both hands pressed against invisible wall, mime performance from behind",
        "half Back view upper body: Model with back to camera, one hand making OK sign, confirmation gesture from behind",
        "half Back view upper body: Back view with both arms raised in surrender position, submission or celebration gesture",
        "half Back view upper body: Standing with back to camera, hands forming binoculars around eyes, searching gesture",
        "half Back view upper body: Back view with one arm flexing bicep muscle, strength demonstration from behind",
        "half Back view upper body: Model with back to camera, both hands on chest in gratitude gesture, emotional pose",
        "half Back view upper body: Back view with one hand making stop gesture palm visible, commanding pose from behind",
        "half Back view upper body: Standing with back to camera, arms crossed low on waist, casual relaxed stance",
        "half Back view upper body: Back view with both hands touching temples in thinking gesture, contemplative pose",
        "half Back view upper body: Model with back to camera, one arm raised checking wrist watch, time-conscious pose",
        "half Back view upper body: Back view with hands making gun gesture pointed upward, playful action pose from behind",
        "half Back view upper body: Standing with back to camera, both arms in welcoming embrace position, open gesture",
        "half Back view upper body: Back view with one hand covering ear in listening gesture, attentive pose from behind",
        "half Back view upper body: Model with back to camera, arms in fist pump celebration, energetic victory pose",
        "half Back view upper body: Back view with both hands forming W shape for win, team spirit gesture from behind",
        "half Back view upper body: Standing with back to camera, one hand making chef's kiss gesture, appreciation from behind",
        "half Back view upper body: Back view with hands counting numbers on fingers, educational gesture from behind",
        "half Back view upper body: Model with back to camera, both arms stretched wide in airplane pose, playful gesture",
        "half Back view upper body: Back view with one hand making L-shape on back of head, self-deprecating gesture from behind",
        "half Back view upper body: Standing with back to camera, hands making quotation marks gesture, expressive pose from behind"
    ]
}

main_data_mapping = {
    "front": [
        "**Half upper body front view**: Model standing in a three-quarter angle pose with body turned slightly to the right while face looks toward the left. Left arm is bent at the elbow with hand inserted into a front pocket. Right arm hangs naturally at the side with a relaxed positioning. Shoulders are squared and slightly pulled back creating an upright, confident posture. Head is turned to the left creating a profile view while maintaining an alert, forward-gazing expression. Overall stance conveys a casual yet poised positioning with weight evenly distributed and torso held straight.",
        "**Half upper body front view**: Model standing in an upright posture with shoulders squared and facing forward. Left arm is positioned down at the side in a relaxed manner. Right arm is bent at the elbow and raised, with the right hand positioned near the upper chest/collar area in a casual, confident gesture. Head is held straight with a slight upward tilt, creating an assured and composed stance. Overall body positioning conveys confidence with a relaxed yet purposeful demeanor.",
        "**Half upper body front view**: Model seated in a relaxed position with torso angled slightly toward the camera. Left arm resting casually across the lap, right hand positioned on the thigh holding an object. Shoulders are relaxed and slightly forward, creating a comfortable, approachable posture. Head tilted upward at a subtle angle with chin raised slightly, conveying confidence. Overall body positioning suggests a casual seated pose with one leg likely drawn up, creating an informal yet poised stance.",
        "**Half upper body front view**: Model standing in a confident pose with left hand placed on hip, right arm relaxed and hanging naturally at side. Body is angled slightly toward the camera with shoulders squared and upright posture. Head is positioned straight forward with a slight tilt. Stance appears stable and grounded with weight evenly distributed. The overall positioning conveys confidence with the classic one-hand-on-hip pose while maintaining a relaxed, approachable demeanor through the natural positioning of the opposite arm.",
        "Half upper body front view: Model standing in a straight, upright posture facing directly forward. Both arms are positioned naturally at the sides with a relaxed stance. Shoulders are square and level, maintaining good posture. The torso is centered and balanced. Both hands appear to be resting in a natural downward position alongside the body. The overall pose conveys a confident, neutral standing position with no tension or dramatic positioning - simply a clean, professional front-facing stance.",
        "Half upper body front view: Model standing in an upright posture with body angled slightly toward the camera. Left arm raised with hand positioned near the collar area at chest level, fingers gently grasping. Right arm relaxed and hanging naturally at the side. Shoulders are squared and level. Head tilted slightly to the right with a subtle turn, creating a confident and composed stance. Overall posture is straight and well-balanced.",
        "**View Type**: Half upper body front view\n\n**Pose Description**: Model standing in an upright, relaxed posture with shoulders squared and facing forward. Both arms are positioned naturally at the sides in a resting stance. The torso is straight with a neutral, comfortable positioning. The head is held upright and centered, facing directly forward. The overall body language conveys a calm, stationary pose with balanced weight distribution and relaxed shoulder positioning.",
        "**Half upper body front view**: Model standing in an upright, confident posture with shoulders squared and facing forward. Both arms are positioned naturally at the sides with hands relaxed and hanging loosely by the hips. The torso is straight and centered, with a slight forward lean that projects confidence. Head is held high with a neutral, composed expression, positioned straight forward with minimal tilt. The overall stance conveys a relaxed yet assured demeanor, with balanced weight distribution and open body language.",
        "**Half upper body front view**: Model standing in a straight, confident posture facing directly forward. Both arms are positioned down at the sides with hands placed on or near the hips in a relaxed but assertive stance. Shoulders are squared and held back, creating an upright, confident bearing. Head is held straight and level, facing forward. The overall body positioning conveys a casual yet self-assured pose with symmetrical arm placement and balanced weight distribution.",
        "**Half upper body front view**: Model standing in an upright posture with both arms positioned at their sides in a relaxed, natural stance. The torso is facing directly forward with shoulders level and squared. The head is positioned straight ahead with a slight upward tilt of the chin. The overall body positioning conveys a confident, stationary pose with balanced weight distribution and relaxed arm placement alongside the torso.",
        "**Half upper body front view**: Model standing in an upright, confident posture with shoulders squared and slightly angled toward the camera. Left arm is bent at the elbow with hand positioned at chest level, appearing to grip or adjust something at the torso. Right arm is relaxed and hanging naturally at the side. Head is turned slightly to the right while maintaining an overall forward-facing orientation. Posture conveys confidence with straight spine and engaged core positioning.",
        "**Half upper body front view**: Model standing in a three-quarter angle pose with body turned slightly to the right while head faces more toward the camera. Left arm is relaxed and hanging naturally at the side with hand partially visible. Right arm is bent at the elbow and positioned across the lower torso area with hand placed near the waist. Shoulders are square and level with an upright, confident posture. Head is held straight with a slight upward tilt, creating a composed and authoritative stance. Overall body positioning conveys a relaxed yet assertive demeanor.",
        "**Half upper body front view**: Model standing in a three-quarter angle pose with body slightly turned to the right while head faces forward and slightly to the left. Both arms are positioned naturally at the sides with hands placed in front pockets. Shoulders are relaxed and squared, maintaining an upright, confident posture. The stance appears balanced with weight evenly distributed, creating a casual yet composed positioning. The head is held straight with a slight leftward gaze, while the torso maintains a natural, relaxed alignment.",
        "**Half upper body front view**: Model standing in a confident, relaxed pose with both hands positioned in front pockets, arms bent at the elbows creating a casual stance. Shoulders are squared and held back in an upright posture. Body is angled slightly toward the camera with a straight, confident stance. Head is held level and facing forward. Overall posture conveys a relaxed yet self-assured positioning with weight evenly distributed.",
        "Half upper body front view: Model standing in a confident three-quarter stance with body angled slightly to the left. Right hand placed firmly on hip with elbow bent outward, left arm relaxed at side. Shoulders are squared and pulled back in an assertive posture. Head turned toward camera with chin slightly raised. Torso positioned at a slight angle rather than completely frontal, creating a dynamic and confident pose. Weight appears evenly distributed with an upright, self-assured stance.",
        "Half upper body front view: Model standing in an upright posture with both arms positioned down at the sides, hands placed in pockets or resting naturally at hip level. Shoulders are squared and facing forward. Head is turned slightly to the left while maintaining an upright neck position. Body displays a relaxed yet confident stance with straight posture and minimal lean. Arms are bent slightly at the elbows with hands positioned low and inward toward the body.",
        "**Half upper body front view**: Model standing in a confident pose with left hand placed on hip, right arm relaxed and hanging naturally at side. Body is angled slightly to the right while maintaining an upright, straight posture. Shoulders are squared and held back in a strong, assertive stance. Head is turned at a slight angle to the left, creating a dynamic three-quarter positioning. Overall posture conveys confidence with a subtle lean that adds visual interest to the composition.",
        "**Half upper body front view**: Model standing in an upright posture with shoulders squared and chest facing forward. Both arms are positioned naturally at the sides with a relaxed stance. The left arm hangs straight down along the body, while the right arm is also at the side but positioned slightly away from the torso. Head is turned approximately 45 degrees to the right, creating a three-quarter profile while maintaining an upright neck position. Overall body positioning conveys a confident, relaxed stance with balanced weight distribution and neutral shoulder alignment.",
        "Half upper body front view: Model standing in a confident stance with left hand placed on hip, right arm positioned across the torso with hand inserted into a front pocket. Body is angled slightly to the right while head is turned to look over the left shoulder. Shoulders are relaxed but squared, with an upright posture displaying a casual yet confident demeanor. The pose creates a dynamic contrast between the body positioning and head direction.",
        "**Half upper body front view**: Model standing in a straight, frontal stance with both arms positioned down at sides, hands inserted into front pockets. Shoulders are squared and level, maintaining an upright, confident posture. Body is centered and facing directly forward with no rotation or lean. Arms are relaxed and bent slightly at the elbows due to the pocket hand placement. Overall stance is balanced and neutral with a natural, comfortable positioning.",
        "**Half upper body front view**: Model standing in an upright, confident posture with shoulders squared and facing forward. Both arms are positioned across the torso with hands clasped together at chest level. The body maintains a straight, formal stance with a slight angular turn to create depth. Head is angled slightly to the right while maintaining forward-facing shoulders. Posture conveys a composed, professional demeanor with arms creating a closed, controlled positioning across the midsection."
    ],

    "side": [
        "**Half side angle upper body**: Model standing in a three-quarter profile position with body angled approximately 45 degrees away from the camera. Head turned back toward the camera over the shoulder, creating a classic over-the-shoulder pose. Arms are relaxed and positioned naturally at the sides. Shoulders are square and level with an upright, confident posture. The stance appears grounded with weight evenly distributed. The overall body positioning suggests a relaxed yet poised demeanor with the head rotation being the primary focal element of the pose.",
        "**Half side angle upper body**: Model standing in a three-quarter profile position with body angled approximately 45 degrees away from the camera. Head turned in profile facing left, creating a clean side silhouette. Arms positioned naturally at sides in a relaxed stance. Shoulders held straight and level with good upright posture. Body weight appears evenly distributed with a confident, neutral standing position. The pose creates a classic side-angle view that emphasizes the profile line from head to torso."
    ],

    "zoomed": [
        "**Zoomed detail view**: Model standing in a neutral, relaxed upright posture with shoulders squared and facing directly forward. Arms are positioned naturally at the sides in a resting stance. Head is held straight and level, maintaining a neutral forward-facing position. Overall body positioning shows a casual, stationary pose with balanced weight distribution and minimal body tension."
    ],

    "full": [
        "**Full body**: Model standing in a straight, upright posture with feet positioned shoulder-width apart in a natural stance. Both arms are relaxed and hanging naturally at the sides with hands positioned loosely by the hips. Shoulders are squared and level, facing directly forward. Head is held upright and centered, looking straight ahead. Body weight appears evenly distributed on both feet with a confident, neutral standing position. Overall posture is relaxed yet composed with no particular lean or angle to the torso.",
        "**Full body**: Model standing in a confident three-quarter pose with body angled slightly to the right. Left arm bent at elbow with hand positioned near waist/hip area in a relaxed gesture. Right arm hanging naturally at side with hand partially clenched. Stance is wide and stable with feet positioned shoulder-width apart. Weight appears evenly distributed on both legs. Torso is upright with shoulders squared and pulled back in a confident posture. Head turned slightly toward camera with chin lifted in an assertive position. Overall body language conveys strength and self-assurance with a casual yet poised stance.",
        "**Full body**: Model seated on stacked circular objects with a casual, relaxed pose. Left leg positioned higher, resting on the upper circular object with foot planted firmly. Right leg positioned lower on the bottom circular object. Left arm resting casually on the raised left knee. Right hand placed down on the lower circular surface for support. Body angled slightly toward the camera with an upright but relaxed posture. Head tilted slightly to one side with a confident, casual stance. Overall positioning creates an asymmetrical, laid-back sitting pose with one leg elevated higher than the other.",
        "Full body: Model standing in a confident three-quarter stance with body angled slightly to the left. Left hand positioned in pocket with elbow bent outward, right arm relaxed at side with hand naturally positioned. Weight distributed evenly on both feet with left foot slightly forward. Shoulders squared and pulled back in an upright, confident posture. Head facing forward toward camera with chin level. Overall stance is relaxed yet poised, with a slight shift of weight creating a natural, casual positioning.",
        "**Full body**: Model standing in a three-quarter pose with body angled slightly to the right. Left arm raised with hand positioned near the collar/neck area in an adjusting gesture. Right arm hanging naturally at the side with hand relaxed. Weight shifted onto the right leg with left leg positioned slightly forward and to the side. Head turned to look off to the left side with chin raised slightly. Shoulders squared but relaxed. Overall posture is upright and confident with a casual, natural stance.",
        "**Full body**: Model standing in a confident, relaxed frontal stance with feet positioned shoulder-width apart. Body weight evenly distributed with a straight, upright posture. Left arm hanging naturally at the side while right arm is bent at the elbow with hand holding an object down by the right hip. Shoulders are square and level, facing directly forward. Head positioned straight ahead with a neutral, composed expression. Overall body positioning conveys a professional, approachable stance with good postural alignment and balanced weight distribution.",
        "Full body: Model standing in a confident, relaxed pose with feet positioned shoulder-width apart in a stable stance. Left hand is casually placed in pocket while right arm hangs naturally at the side. Body weight appears evenly distributed with a slight lean toward the camera. Shoulders are squared and held back in an upright, confident posture. Head is positioned straight forward with chin level. Overall stance conveys a casual yet self-assured positioning with good postural alignment and balanced weight distribution through both legs.",
        "**Full body**: Model seated on a stool with left leg positioned forward and right leg slightly back, both feet planted on the ground. Body is angled three-quarters toward the camera with a confident, relaxed posture. Left hand rests casually on the left thigh, while the right hand is positioned on the right thigh. Shoulders are squared and slightly back, creating an open chest position. Head is turned slightly to the right side with chin lifted at a confident angle. Overall stance conveys a relaxed yet assured sitting pose with good posture and balanced weight distribution.",
        "**Full body**: Model standing in a confident, relaxed pose with feet positioned shoulder-width apart in a stable stance. Left arm is bent at the elbow with hand placed casually in pocket. Right arm hangs naturally at the side with hand also positioned in or near the pocket area. Body weight is evenly distributed with a slight shift toward the left leg. Shoulders are squared and level, maintaining good posture. Head is held upright and facing forward with a slight downward gaze angle. Overall posture conveys a casual, confident demeanor with an upright spine and relaxed positioning."
    ],

    "back": [
        "**Half Back view upper body**: Model standing in a three-quarter back view position with body angled away from camera, head turned in profile facing right side, shoulders squared and relaxed, arms hanging naturally at sides with hands positioned near hip level, upright posture with straight spine, weight evenly distributed, slight turn of torso creating a dynamic back-facing stance.",
        "**Half Back view upper body**: Model standing in an upright posture with back turned toward the camera, head turned to the right side showing partial profile, shoulders relaxed and squared, arms hanging naturally at sides with hands not visible, spine straight with confident neutral stance, body weight evenly distributed, slight three-quarter angle allowing partial side visibility while maintaining primarily rear-facing orientation.",
        "**Half Back view upper body**: Model standing in a three-quarter back pose with body angled away from camera, head turned in profile facing left, arms hanging naturally at sides with hands positioned straight down, shoulders relaxed and level, upright posture with straight spine, weight evenly distributed on both feet in a neutral standing stance.",
        "**Half Back view upper body**: Model standing in a three-quarter back pose with body angled away from camera, head turned in profile facing left side. Arms positioned naturally at sides with slight bend at the elbows. Shoulders are relaxed and squared, maintaining an upright posture. The stance appears confident and stable with weight evenly distributed. Head positioning shows a clean side profile angle while the torso remains turned away, creating a dynamic contrast between the head and body positioning.",
        "**Half Back view upper body**: Model standing in a three-quarter back pose with body angled away from camera, head turned in profile to the left side. Shoulders are relaxed and squared, with arms hanging naturally at the sides. Left arm is positioned slightly away from the torso, while right arm appears more relaxed against the body. Posture is upright and confident with a straight spine. The stance appears stable with weight evenly distributed, creating a casual yet composed positioning that showcases the back and side profile of the upper torso.",
        "**Half Back view upper body**: Model standing in an upright posture facing away from camera, both arms positioned down at sides with hands placed on hips, elbows bent outward creating angular arm positioning, shoulders held back and squared, head turned completely away showing back of head and neck, confident stance with straight spine and balanced weight distribution.",
        "**Half Back view upper body**: Model standing in a three-quarter back pose with body angled away from camera, head turned in profile facing left side, shoulders squared and held back in confident posture, both arms hanging naturally at sides with hands relaxed, upright stance with straight spine, weight evenly distributed, overall posture displaying a calm, composed positioning while maintaining an over-the-shoulder perspective.",
        "**Half Back view upper body**: Model standing in a three-quarter back view position with body angled away from camera, head turned in profile to the left side, shoulders slightly hunched forward, arms hanging naturally at sides with hands not visible (likely in pockets or at sides), posture relaxed and casual with slight forward lean, weight distributed evenly on both feet in a natural standing stance."
    ]
}

garment_upload_type = "upper_garment"
age_group = "young adult"
gender = "male"
ethnicity = "indian"
height = "average"
width = "average"
fitting = "regular fit"
selected_background = "78.webp"
age = "25"
upper_garment_type = "boy jacket"
upper_garment_specs = ""
lower_garment_specs = ""
lower_garment_type = "boy jeans"

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

def photoshoot_generation(garment_image_path):
    try:
        pose_data_mapping=main_data_mapping
        photoshoot_id = str(uuid.uuid4())
        pose_descriptions=[]
        pose_descriptions.extend(random.sample(pose_data_mapping["front"], 2))
        pose_descriptions.extend(random.sample(pose_data_mapping["back"], 2))
        pose_descriptions.extend(random.sample(pose_data_mapping["side"], 2))
        pose_descriptions.extend(random.sample(pose_data_mapping["zoomed"], 1))
        pose_descriptions.extend(random.sample(pose_data_mapping["full"], 2))

        os.makedirs(f"output_image/{photoshoot_id}", exist_ok=True)

        garmentdescription = ""
        if upper_garment_specs:
            garmentdescription += f" Upper garment details: {upper_garment_specs}"
        if lower_garment_specs:
            garmentdescription += f" Lower garment details: {lower_garment_specs}"

        parts = []
        exten = garment_image_path.split(".")[-1]
        if exten.lower() in ["jpg", "jpeg"]:
            exten = "jpeg"
        upper_garment_path = f"input_image/{garment_image_path}"
        with open(upper_garment_path, "rb") as f:
            upper_image_data = f.read()

        parts.append(types.Part.from_bytes(
            mime_type=f"image/{exten.lower()}",
            data=upper_image_data,
        ))

        generated_first_image_path = ""
        for unique_num, pose_detail in enumerate(pose_descriptions):
            if unique_num == 0:
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
                            - NO creative interpretation or modifications allowed
                            - Maintain authentic draping and fabric behavior
    
                            MODEL SPECIFICATIONS (MUST REMAIN CONSISTENT):
                            - Age: {age} years ({age_group})
                            - Ethnicity: {ethnicity}
                            - Gender: {gender}
                            - Height: {height}
                            - Build: {width}
                            - Professional fashion model appearance with natural, authentic expression
    
                            GARMENT SPECIFICATIONS (EXACT REPLICATION REQUIRED):
                            {garmentdescription}
    
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
                if generated_first_image_path and unique_num == 1:
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
                    base_image_filename = f"output_image/{photoshoot_id}/{output_filename}"
                    image.save(base_image_filename)
                    upscaled_filename = f"output_image/{photoshoot_id}/upscaled_{output_filename}"
                    response_upscale = upscale_image(base_image_filename, upscaled_filename)

                    if unique_num == 0:
                        generated_first_image_path = base_image_filename
                        parts.pop()
                        parts.pop()
                    else:
                        parts.pop()

    except Exception as e:
        print(f"An error occurred: {e}")

folder_path = "input_image"  # change this

# Get all files and directories
all_items = os.listdir(folder_path)

# Filter only files
files = [f for f in all_items if os.path.isfile(os.path.join(folder_path, f))]

print("Files in folder:")
for file in files:
    photoshoot_generation(file)
