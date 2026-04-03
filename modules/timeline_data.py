# modules/timeline_data.py
# Day-by-day / week-by-week timeline data for the Journey Dashboard
# This module contains all the structured timeline content for:
#   - Pregnancy (40 weeks)
#   - Trying to Conceive / TTC (30 cycle days)
#   - Parent / Postpartum (0-24 months)

from typing import List, Dict, Any, Optional


def get_trimester(week: int) -> int:
    if week <= 12:
        return 1
    elif week <= 27:
        return 2
    return 3


def get_trimester_color(trimester: int) -> tuple:
    """Returns (gradient_color, text_color) for each trimester."""
    if trimester == 1:
        return ("from-green-100 to-emerald-200", "text-green-700")
    elif trimester == 2:
        return ("from-purple-100 to-purple-200", "text-purple-700")
    return ("from-pink-100 to-rose-200", "text-rose-700")


# ════════════════════════════════════════════════════════════════════════════
#  PREGNANCY TIMELINE — 40 Weeks
# ════════════════════════════════════════════════════════════════════════════

PREGNANCY_TIMELINE: List[Dict[str, Any]] = [
    {
        "id": 1, "label": "Preparing", "emoji": "🌱",
        "tip": "Your body is getting ready. Track your cycle and take folic acid.",
        "size": None, "fruit": None,
        "actionItem": "Start taking 400mcg folic acid daily.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
    },
    {
        "id": 2, "label": "Ovulation Window", "emoji": "🌱",
        "tip": "Ovulation may happen this week — prime time for conception!",
        "size": None, "fruit": None,
        "actionItem": "Track your basal body temperature.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
    },
    {
        "id": 3, "label": "Conception", "emoji": "✨",
        "tip": "Fertilization may happen now. The magic begins!",
        "size": None, "fruit": None,
        "actionItem": "Continue prenatal vitamins. Avoid alcohol.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
    },
    {
        "id": 4, "label": "Implanting", "emoji": "🫘",
        "tip": "The embryo implants in the uterine wall. You may miss your period.",
        "size": "1-2 mm", "fruit": "Poppy Seed",
        "actionItem": "Take a home pregnancy test if your period is late.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/poppyseed.png",
    },
    {
        "id": 5, "label": "Heart Forms", "emoji": "💓",
        "tip": "Baby's heart tube starts forming. Neural tube developing rapidly.",
        "size": "3-5 mm", "fruit": "Sesame Seed",
        "actionItem": "Schedule your first prenatal appointment.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/sesameseed.png",
    },
    {
        "id": 6, "label": "Heartbeat!", "emoji": "💓",
        "tip": "Heartbeat may be detectable on ultrasound! Morning sickness may begin.",
        "size": "5-7 mm", "fruit": "Lentil",
        "actionItem": "Eat small, frequent meals to manage nausea.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/lentil.png",
    },
    {
        "id": 7, "label": "Growing Fast", "emoji": "🫐",
        "tip": "Brain and face developing rapidly. Baby is doubling in size.",
        "size": "10-13 mm", "fruit": "Blueberry",
        "actionItem": "Stay hydrated — aim for 8-10 glasses of water daily.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/blueberry.png",
    },
    {
        "id": 8, "label": "Tiny Moves", "emoji": "🍇",
        "tip": "Baby starts to move! Fingers and toes are forming. First ultrasound time.",
        "size": "1.6 cm", "fruit": "Raspberry",
        "actionItem": "Schedule your dating scan (8-12 weeks).",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/raspberry.png",
    },
    {
        "id": 9, "label": "Organs Form", "emoji": "🍇",
        "tip": "All major organs are forming. Eyes are present but fused shut.",
        "size": "2.3 cm", "fruit": "Grape",
        "actionItem": "Eat iron-rich foods: spinach, lentils, pomegranate.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/grape.png",
    },
    {
        "id": 10, "label": "Fingers & Toes", "emoji": "🍊",
        "tip": "Tiny fingers and toes appear. Vital organs starting to function.",
        "size": "3.1 cm", "fruit": "Kumquat",
        "actionItem": "Take your prenatal vitamins daily without fail.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/kumquat.png",
    },
    {
        "id": 11, "label": "Baby Moves", "emoji": "🍈",
        "tip": "Baby can stretch and somersault! Head is half of body length.",
        "size": "4.1 cm", "fruit": "Fig",
        "actionItem": "Announce to your family if you feel comfortable.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/fig.png",
    },
    {
        "id": 12, "label": "NT Scan Time", "emoji": "🍋",
        "tip": "Schedule your NT scan. Nausea may improve soon! End of first trimester approaching.",
        "size": "5.4 cm", "fruit": "Lime",
        "actionItem": "Schedule your NT (Nuchal Translucency) ultrasound scan.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG / FOGSI Guidelines",
        "imageUrl": "/assets/fruits/lime.png",
    },
    {
        "id": 13, "label": "Second Trimester!", "emoji": "🍋",
        "tip": "Welcome to trimester 2! Energy starts returning. Vocal cords developing.",
        "size": "7.4 cm", "fruit": "Lemon",
        "actionItem": "Share the good news — miscarriage risk drops significantly.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/lemon.png",
    },
    {
        "id": 14, "label": "Facial Features", "emoji": "🍑",
        "tip": "Baby can squint and frown. Your bump may start to show!",
        "size": "8.7 cm", "fruit": "Nectarine",
        "actionItem": "Start wearing comfortable, stretchy clothing.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/nectarine.png",
    },
    {
        "id": 15, "label": "Taste Buds", "emoji": "🍎",
        "tip": "Baby develops taste buds and can sense light now. Eat varied foods!",
        "size": "10.1 cm", "fruit": "Apple",
        "actionItem": "Eat a rainbow of fruits and vegetables for micronutrients.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/apple.png",
    },
    {
        "id": 16, "label": "Hearing Begins", "emoji": "🥑",
        "tip": "Baby starts hearing your voice. You might start feeling movement soon.",
        "size": "11.6 cm", "fruit": "Avocado",
        "actionItem": "Talk and sing to your baby — they can hear you now!",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/avocado.png",
    },
    {
        "id": 17, "label": "Skeleton Hardens", "emoji": "🍐",
        "tip": "Skeleton is hardening from cartilage to bone. You may feel flutters.",
        "size": "13 cm", "fruit": "Pear",
        "actionItem": "Increase calcium intake: milk, curd, ragi.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/pear.png",
    },
    {
        "id": 18, "label": "Anomaly Scan", "emoji": "🫑",
        "tip": "Anomaly scan (TIFFA) possible now. Nerves developing myelin.",
        "size": "14.2 cm", "fruit": "Bell Pepper",
        "actionItem": "Schedule your TIFFA / Anomaly Scan (18-20 weeks).",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "FOGSI Guidelines",
        "imageUrl": "/assets/fruits/pepper.png",
    },
    {
        "id": 19, "label": "Vernix Coating", "emoji": "🍅",
        "tip": "Protective vernix coating forms on skin. Senses developing.",
        "size": "15.3 cm", "fruit": "Heirloom Tomato",
        "actionItem": "Stay active with gentle exercise like walking or prenatal yoga.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/tomato.png",
    },
    {
        "id": 20, "label": "Halfway! 🎉", "emoji": "🍌",
        "tip": "Halfway there! Baby can swallow amniotic fluid now.",
        "size": "16.4 cm", "fruit": "Banana",
        "actionItem": "Celebrate the halfway mark! Review your birth plan options.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/banana.png",
    },
    {
        "id": 21, "label": "Active Baby", "emoji": "🥕",
        "tip": "Movements get stronger. Eyebrows and eyelids are present!",
        "size": "26.7 cm", "fruit": "Carrot",
        "actionItem": "Start counting kicks — aim for 10 movements in 2 hours.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/carrot.png",
    },
    {
        "id": 22, "label": "Taste Buds Active", "emoji": "🍈",
        "tip": "Baby's taste buds are active. Eyelids can open partially.",
        "size": "27.8 cm", "fruit": "Spaghetti Squash",
        "actionItem": "Eat diverse, flavorful Indian meals — baby tastes them too!",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/squash.png",
    },
    {
        "id": 23, "label": "Hearing Established", "emoji": "🥭",
        "tip": "Hearing is well established. Baby responds to sounds and music.",
        "size": "28.9 cm", "fruit": "Large Mango",
        "actionItem": "Play soothing music. Practice deep breathing exercises.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/mango.png",
    },
    {
        "id": 24, "label": "Viability Milestone", "emoji": "🌽",
        "tip": "Important milestone: viability outside womb. Lungs developing branches. GD test time.",
        "size": "30 cm", "fruit": "Ear of Corn",
        "actionItem": "Take your Glucose Tolerance Test (GTT) for gestational diabetes.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG / FOGSI Guidelines",
        "imageUrl": "/assets/fruits/corn.png",
    },
    {
        "id": 25, "label": "Hair Grows", "emoji": "🥬",
        "tip": "Baby has hair! Skin is becoming less transparent.",
        "size": "34.6 cm", "fruit": "Rutabaga",
        "actionItem": "Monitor weight gain. Aim for balanced nutrition.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/rutabaga.png",
    },
    {
        "id": 26, "label": "Eyes Open", "emoji": "🥬",
        "tip": "Eyes fully open now. Baby responds to light!",
        "size": "35.6 cm", "fruit": "Scallion",
        "actionItem": "Sleep on your left side for optimal blood flow to baby.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/scallion.png",
    },
    {
        "id": 27, "label": "Brain Surge", "emoji": "🥦",
        "tip": "Brain is very active. Welcome to the third trimester!",
        "size": "36.6 cm", "fruit": "Cauliflower",
        "actionItem": "Eat omega-3 rich foods: walnuts, flaxseed, fish oil.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/cauliflower.png",
    },
    {
        "id": 28, "label": "Third Trimester!", "emoji": "🍆",
        "tip": "Final trimester begins! Baby can dream (REM sleep). Weighs ~1 kg.",
        "size": "37.6 cm", "fruit": "Eggplant",
        "actionItem": "Start preparing your hospital bag checklist.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/eggplant.png",
    },
    {
        "id": 29, "label": "Bones Harden", "emoji": "🍈",
        "tip": "Bones are fully developed and hardening. Your back may ache.",
        "size": "38.6 cm", "fruit": "Butternut Squash",
        "actionItem": "Use a pregnancy pillow for better sleep comfort.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/butternut.png",
    },
    {
        "id": 30, "label": "Memory Starts", "emoji": "🥬",
        "tip": "Baby's memory is starting to work. Gains weight rapidly.",
        "size": "39.9 cm", "fruit": "Cabbage",
        "actionItem": "Attend antenatal classes if available at your hospital.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/cabbage.png",
    },
    {
        "id": 31, "label": "Brain Connections", "emoji": "🥥",
        "tip": "Brain making billions of connections. Reproductive organs fully formed.",
        "size": "41.1 cm", "fruit": "Coconut",
        "actionItem": "Rest well. Avoid standing for long periods.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/coconut.png",
    },
    {
        "id": 32, "label": "Position Check", "emoji": "🍈",
        "tip": "Baby may turn head-down. Practicing breathing motions.",
        "size": "42.4 cm", "fruit": "Jicama",
        "actionItem": "Start packing your hospital bag!",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/jicama.png",
    },
    {
        "id": 33, "label": "Immune System", "emoji": "🍍",
        "tip": "Immune system developing. Consider your birth plan.",
        "size": "43.7 cm", "fruit": "Pineapple",
        "actionItem": "Discuss your birth plan with your OB-GYN.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/pineapple.png",
    },
    {
        "id": 34, "label": "Lungs Maturing", "emoji": "🍈",
        "tip": "Lungs nearly mature. Vernix is getting thicker.",
        "size": "45 cm", "fruit": "Cantaloupe",
        "actionItem": "Practice Lamaze breathing and relaxation techniques.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/cantaloupe.png",
    },
    {
        "id": 35, "label": "Head Down", "emoji": "🍈",
        "tip": "Baby usually settles head-down. Kidneys fully developed. Less room to move.",
        "size": "46.2 cm", "fruit": "Honeydew Melon",
        "actionItem": "Note any change in baby's movement patterns and report to doctor.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/honeydew.png",
    },
    {
        "id": 36, "label": "Almost Ready", "emoji": "🥬",
        "tip": "Baby is almost ready! Shedding lanugo. Nesting instinct kicks in.",
        "size": "47.4 cm", "fruit": "Romaine Lettuce",
        "actionItem": "Finalize your hospital bag. Install the car seat.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/lettuce.png",
    },
    {
        "id": 37, "label": "Early Term", "emoji": "🥬",
        "tip": "Baby is early term. Lungs and brain still maturing.",
        "size": "48.6 cm", "fruit": "Swiss Chard",
        "actionItem": "Know the signs of labour: contractions, water breaking.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/chard.png",
    },
    {
        "id": 38, "label": "Full Term!", "emoji": "🥬",
        "tip": "Baby is full term! Systems are ready for the world.",
        "size": "49.8 cm", "fruit": "Leek",
        "actionItem": "Keep your hospital bag by the door. Stay close to your hospital.",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/leek.png",
    },
    {
        "id": 39, "label": "Final Prep", "emoji": "🍉",
        "tip": "Baby is fully developed. Watch for labour signs! Waiting for hello day!",
        "size": "50.7 cm", "fruit": "Watermelon",
        "actionItem": "Walk gently. Stay calm and positive. Your baby is almost here!",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/watermelon.png",
    },
    {
        "id": 40, "label": "Due Date! 🎉", "emoji": "🎃",
        "tip": "Your due date is here! Baby is ready to meet you! Happy Due Date!",
        "size": "51.2 cm", "fruit": "Pumpkin",
        "actionItem": "If no labour yet, discuss next steps with your doctor. Stay patient!",
        "expertReviewedBy": "Medical Advisory Board",
        "source": "ACOG Guidelines",
        "imageUrl": "/assets/fruits/pumpkin.png",
    },
]


# ════════════════════════════════════════════════════════════════════════════
#  TTC (TRYING TO CONCEIVE) TIMELINE — 30 Cycle Days
# ════════════════════════════════════════════════════════════════════════════

TTC_TIMELINE: List[Dict[str, Any]] = [
    {"id": 1, "label": "Menstruation", "emoji": "🔴", "tip": "Period begins. Rest and stay hydrated.", "isFertile": False, "actionItem": "Track Day 1 in your cycle tracker app.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 2, "label": "Menstruation", "emoji": "🔴", "tip": "Light exercise like walking can help cramps.", "isFertile": False, "actionItem": "Take iron-rich foods: spinach, dates, jaggery.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 3, "label": "Menstruation", "emoji": "🔴", "tip": "Iron-rich foods help replenish blood loss.", "isFertile": False, "actionItem": "Eat leafy greens, lentils, and pomegranate juice.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 4, "label": "Menstruation", "emoji": "🔴", "tip": "Flow may lighten. Stay nourished.", "isFertile": False, "actionItem": "Continue your daily folic acid supplement (400mcg).", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 5, "label": "Menstruation", "emoji": "🔴", "tip": "Period ending. Your body starts the rebuild.", "isFertile": False, "actionItem": "Start observing cervical mucus changes.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 6, "label": "Follicular Phase", "emoji": "🌸", "tip": "Follicles developing. Estrogen rising.", "isFertile": False, "actionItem": "Eat protein-rich foods: eggs, paneer, dal.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 7, "label": "Follicular Phase", "emoji": "🌸", "tip": "Uterine lining rebuilding. Energy increases!", "isFertile": False, "actionItem": "Great time for exercise. Build up your body.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 8, "label": "Follicular Phase", "emoji": "🌿", "tip": "Great time for exercise. Build up your body.", "isFertile": False, "actionItem": "Consider CoQ10 supplementation for egg quality.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 9, "label": "Follicular Phase", "emoji": "🌿", "tip": "Consider taking CoQ10 for egg quality.", "isFertile": False, "actionItem": "Stay stress-free. Try meditation or deep breathing.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 10, "label": "Pre-Fertile", "emoji": "🌟", "tip": "Fertility window approaching! Start observing cervical mucus.", "isFertile": False, "actionItem": "Begin checking cervical mucus daily.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 11, "label": "Fertile Window Opens", "emoji": "🌟", "tip": "Cervical mucus may become watery — sign of approaching ovulation.", "isFertile": True, "actionItem": "Begin having intercourse every other day.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 12, "label": "Fertile Window", "emoji": "✨", "tip": "🔥 Fertile! Egg-white cervical mucus is a great sign.", "isFertile": True, "actionItem": "Have intercourse today. Sperm can survive 3-5 days.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 13, "label": "Peak Fertile Day", "emoji": "🔥", "tip": "🔥 Peak fertility! Highest chance of conception today.", "isFertile": True, "actionItem": "Have intercourse today or tomorrow for best chances.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 14, "label": "Ovulation Day", "emoji": "🥚", "tip": "🥚 Ovulation! Egg released from the ovary — timing matters now.", "isFertile": True, "actionItem": "Have intercourse today. Egg survives only 12-24 hours.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 15, "label": "Post-Ovulation", "emoji": "✨", "tip": "Still fertile for ~12 hours. Then begins the two-week wait.", "isFertile": True, "actionItem": "Rest. Avoid heavy lifting or intense exercise.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 16, "label": "Luteal Phase", "emoji": "🌙", "tip": "Progesterone rises. Basal body temperature may increase.", "isFertile": False, "actionItem": "Log your basal body temperature each morning.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 17, "label": "Luteal Phase", "emoji": "🌙", "tip": "Possible implantation starting. Stay calm and positive.", "isFertile": False, "actionItem": "Avoid alcohol and excessive caffeine.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 18, "label": "Luteal Phase", "emoji": "🌙", "tip": "Avoid alcohol & excessive caffeine during the wait.", "isFertile": False, "actionItem": "Keep taking folic acid daily (400mcg).", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 19, "label": "Implantation Window", "emoji": "🌙", "tip": "Implantation may occur around now. Light spotting is possible and normal.", "isFertile": False, "actionItem": "Don't panic if you see light spotting — it can be implantation.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 20, "label": "Luteal Phase", "emoji": "🌙", "tip": "Keep taking folic acid daily (400mcg).", "isFertile": False, "actionItem": "Stay hydrated and eat well.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 21, "label": "Luteal Phase", "emoji": "🌙", "tip": "Possible early pregnancy signs: tender breasts, fatigue.", "isFertile": False, "actionItem": "Note any early symptoms but don't over-analyze.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 22, "label": "Luteal Phase", "emoji": "🌙", "tip": "Stay positive. The two-week wait is hard but you've got this.", "isFertile": False, "actionItem": "Distract yourself with a hobby or gentle exercise.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 23, "label": "Luteal Phase", "emoji": "🌙", "tip": "Fatigue may increase. Rest when you can.", "isFertile": False, "actionItem": "Go to bed early. Sleep is essential for hormonal balance.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 24, "label": "Luteal Phase", "emoji": "🌙", "tip": "Some feel bloated or crampy — this is normal either way.", "isFertile": False, "actionItem": "Avoid heavy meals. Eat fibre-rich foods.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 25, "label": "Late Luteal", "emoji": "🤞", "tip": "Early HPT may show a faint line for some. Don't test too early!", "isFertile": False, "actionItem": "Wait until Day 28 for the most accurate test result.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 26, "label": "Late Luteal", "emoji": "🤞", "tip": "Watching for signs? Stay calm and patient.", "isFertile": False, "actionItem": "Prepare emotionally for either outcome. Both are okay.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 27, "label": "Late Luteal", "emoji": "🤞", "tip": "HPT may work now if your period is late.", "isFertile": False, "actionItem": "Use first-morning urine for the most accurate test.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 28, "label": "Test Day", "emoji": "🧪", "tip": "Period expected today. Take a pregnancy test!", "isFertile": False, "actionItem": "Take a home pregnancy test with first-morning urine.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 29, "label": "Late?", "emoji": "🌈", "tip": "Period late? Retest in 2-3 days if first test was negative.", "isFertile": False, "actionItem": "If negative, wait 3 days and retest. If positive, call your OB!", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
    {"id": 30, "label": "Result Day", "emoji": "🌈", "tip": "If positive — congratulations! 🎉 Book your first OB appointment.", "isFertile": False, "actionItem": "Schedule a blood test (beta-hCG) to confirm pregnancy.", "expertReviewedBy": "Dr. Priya Sharma, Fertility Specialist", "source": "WHO Fertility Guidelines"},
]


# ════════════════════════════════════════════════════════════════════════════
#  PARENT TIMELINE — 0 to 24 Months
# ════════════════════════════════════════════════════════════════════════════

PARENT_TIMELINE: List[Dict[str, Any]] = [
    {"id": 0, "label": "Newborn", "emoji": "👶", "tip": "Skin-to-skin contact is crucial. Feed every 2-3 hours.", "vaccine": "BCG, OPV-0, Hep-B1", "actionItem": "Focus on skin-to-skin bonding. Initiate breastfeeding within 1 hour.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 1, "label": "First Smiles", "emoji": "😊", "tip": "Baby starts social smiling! Begin gentle tummy time.", "vaccine": None, "actionItem": "Start daily tummy time — 3-5 minutes, 2-3 times a day.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 2, "label": "Tracking Eyes", "emoji": "👀", "tip": "Eyes follow objects. Coos and gurgles begin!", "vaccine": "DPT-1, IPV-1, Hep-B2, Hib-1, Rota-1, PCV-1", "actionItem": "Get the 6-week vaccination set done on time.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 3, "label": "Head Control", "emoji": "💪", "tip": "Holds head up during tummy time. Loves looking at faces!", "vaccine": None, "actionItem": "Increase tummy time to 10-15 minutes per session.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 4, "label": "Rolling Over", "emoji": "🔄", "tip": "May roll tummy to back! Laughs out loud.", "vaccine": "DPT-2, IPV-2, Hib-2, Rota-2, PCV-2", "actionItem": "Get the 14-week vaccination set. Baby-proof the sleeping area.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 5, "label": "Ready for Solids?", "emoji": "🥄", "tip": "Shows interest in food you eat. Wait until 6 months to start.", "vaccine": None, "actionItem": "Do NOT start solids yet. Exclusive breastfeeding until 6 months.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "WHO / IAP Feeding Guidelines"},
    {"id": 6, "label": "Solid Food Begins!", "emoji": "🍚", "tip": "Start complementary foods! Begin with rice cereal, dal water, mashed banana.", "vaccine": "DPT-3, IPV-3, Hib-3, Rota-3, PCV-3, Hep-B3", "actionItem": "Introduce one new food at a time. Wait 3 days before adding another.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "WHO / IAP Complementary Feeding Guidelines"},
    {"id": 7, "label": "Sitting Up", "emoji": "🧒", "tip": "Sits without support! Introduce mashed veggies and khichdi.", "vaccine": None, "actionItem": "Give mashed foods with a spoon. Avoid honey until 1 year.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Feeding Guidelines"},
    {"id": 8, "label": "Crawling", "emoji": "🐛", "tip": "May start crawling! Baby-proof your entire home.", "vaccine": None, "actionItem": "Cover electrical outlets. Remove small objects from baby's reach.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Safety Guidelines"},
    {"id": 9, "label": "First Words", "emoji": "🗣️", "tip": "'Mama' / 'Dada' sounds! Understands 'no'. Claps hands.", "vaccine": "Measles-1 (MR vaccine at 9 months)", "actionItem": "Get the 9-month Measles vaccine. Read simple picture books daily.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 10, "label": "Standing", "emoji": "🧍", "tip": "Pulls to stand using furniture. Points at things. Waves bye!", "vaccine": None, "actionItem": "Encourage standing but don't force walking. Every baby has their pace.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 11, "label": "Cruising", "emoji": "🚶", "tip": "Walks holding furniture. Time for finger foods!", "vaccine": None, "actionItem": "Introduce small finger foods like soft idli pieces, cheese cubes.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Feeding Guidelines"},
    {"id": 12, "label": "First Birthday! 🎂", "emoji": "🎂", "tip": "May take first steps! 🎉 Says 1-3 words clearly.", "vaccine": "Hep-A1, MMR-1", "actionItem": "Get the 12-month vaccines. Celebrate this amazing milestone!", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 13, "label": "Walking", "emoji": "👣", "tip": "Walking gets steadier. Scribbles with crayons!", "vaccine": None, "actionItem": "Let baby walk barefoot at home for better balance.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 14, "label": "More Words", "emoji": "💬", "tip": "Vocabulary grows. Points to body parts when asked.", "vaccine": None, "actionItem": "Name everything you see on walks. Talk, talk, talk!", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 15, "label": "Independence", "emoji": "🌟", "tip": "Wants to do things alone. Stacks 2-3 blocks.", "vaccine": "PCV Booster", "actionItem": "Get the PCV booster vaccine. Provide safe stacking toys.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 16, "label": "Booster Time", "emoji": "💉", "tip": "Booster vaccines due. Baby runs and climbs!", "vaccine": "DPT-B1, IPV-B1, Hib-B", "actionItem": "Complete all booster vaccines on schedule.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 17, "label": "Imagination", "emoji": "🎭", "tip": "Pretend play begins! Feeds a doll, talks to toys.", "vaccine": None, "actionItem": "Encourage imaginative play. Join in their pretend world.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 18, "label": "Two-Word Sentences", "emoji": "📝", "tip": "Two-word sentences: 'Want milk'. Knows 10+ words.", "vaccine": "Hep-A2", "actionItem": "Get the Hepatitis A second dose. Read stories before bedtime.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
    {"id": 19, "label": "Running", "emoji": "🏃", "tip": "Runs with confidence. Loves copying adults.", "vaccine": None, "actionItem": "Let them help with simple chores: wiping table, putting toys away.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 20, "label": "Social Play", "emoji": "🤝", "tip": "Plays alongside other kids. Beginning to show empathy.", "vaccine": None, "actionItem": "Arrange playdates. Teach sharing with gentle guidance.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 21, "label": "Colors & Shapes", "emoji": "🔵", "tip": "Starts recognizing colors and simple shapes.", "vaccine": None, "actionItem": "Use colorful toys and books to teach colours through play.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 22, "label": "Potty Signs", "emoji": "🚽", "tip": "May show readiness signs for potty training.", "vaccine": None, "actionItem": "If showing signs: watch for a dry nappy for 2+ hours, introduce a potty.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 23, "label": "Storytelling", "emoji": "📚", "tip": "Loves stories! Can answer simple questions.", "vaccine": None, "actionItem": "Read 2-3 picture books daily. Ask 'what's this?' questions.", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Growth & Development Guidelines"},
    {"id": 24, "label": "Two Years Old! 🎉", "emoji": "🎉", "tip": "Happy 2nd birthday! 🎂 50+ words, jumps, kicks ball.", "vaccine": "DPT-B2, IPV-B2, MMR-2, Varicella", "actionItem": "Complete the 2-year vaccination schedule. Celebrate your toddler!", "expertReviewedBy": "IAP (Indian Academy of Pediatrics)", "source": "IAP Immunization Guidelines"},
]


# ════════════════════════════════════════════════════════════════════════════
#  PUBLIC API FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════

def get_timeline_for_stage(stage: str) -> Optional[Dict[str, Any]]:
    """
    Returns the full timeline data for a given journey stage.
    stage: 'pregnant', 'ttc', or 'parent'
    Returns dict with 'items' key containing the timeline list,
    or None if stage is invalid.
    """
    stage_lower = stage.lower().strip()

    if stage_lower == "pregnant":
        items = []
        for week_data in PREGNANCY_TIMELINE:
            trimester = get_trimester(week_data["id"])
            color, text_color = get_trimester_color(trimester)
            items.append({
                **week_data,
                "trimester": trimester,
                "color": color,
                "textColor": text_color,
            })
        return {"stage": "PREGNANT", "items": items}

    elif stage_lower == "ttc":
        items = []
        for day_data in TTC_TIMELINE:
            day = day_data["id"]
            is_fertile = day_data.get("isFertile", False)
            if is_fertile:
                color = "from-amber-100 to-orange-200"
                text_color = "text-orange-700"
            elif day <= 5:
                color = "from-red-100 to-pink-200"
                text_color = "text-red-700"
            elif day <= 9:
                color = "from-pink-100 to-rose-200"
                text_color = "text-pink-700"
            else:
                color = "from-purple-100 to-violet-200"
                text_color = "text-purple-700"
            items.append({
                **day_data,
                "color": color,
                "textColor": text_color,
            })
        return {"stage": "TTC", "items": items}

    elif stage_lower == "parent":
        items = []
        for m_data in PARENT_TIMELINE:
            month = m_data["id"]
            if month < 6:
                color = "from-pink-100 to-pink-200"
                text_color = "text-pink-700"
            elif month < 12:
                color = "from-orange-100 to-amber-200"
                text_color = "text-orange-700"
            else:
                color = "from-green-100 to-teal-200"
                text_color = "text-teal-700"
            items.append({
                **m_data,
                "color": color,
                "textColor": text_color,
            })
        return {"stage": "PARENT", "items": items}

    return None
