#!/bin/bash
# Tripitaka Scraping Commands - Run these one by one

echo "🚀 TRIPITAKA SCRAPING COMMANDS"
echo "================================"
echo ""

echo "📚 Available Nikayas:"
echo "1. digha    - දීඝ නිකාය (17-264)      ~248 suttas"
echo "2. majjhima - මජ්ඣිම නිකාය (265-979)    ~715 suttas" 
echo "3. samyutta - සංයුත්ත නිකාය (980-1172)  ~193 suttas"
echo "4. khuddaka - ඛුද්දක නිකාය (1173-5756) ~4,584 suttas"
echo "5. anguttara- අංගුත්තර නිකාය (5757-15702) ~9,946 suttas"
echo ""

echo "🔧 COMMANDS TO RUN (copy and paste one by one):"
echo ""

echo "# 1. Scrape දීඝ නිකාය (Dīgha Nikāya) - Long Discourses"
echo "python main.py --mode nikaya --nikaya digha --raw --batch-size 50 --delay 1.0"
echo ""

echo "# 2. Scrape මජ්ඣිම නිකාය (Majjhima Nikāya) - Middle Length Discourses"  
echo "python main.py --mode nikaya --nikaya majjhima --raw --batch-size 50 --delay 1.0"
echo ""

echo "# 3. Scrape සංයුත්ත නිකාය (Saṃyutta Nikāya) - Connected Discourses"
echo "python main.py --mode nikaya --nikaya samyutta --raw --batch-size 50 --delay 1.0"
echo ""

echo "# 4. Scrape ඛුද්දක නිකාය (Khuddaka Nikāya) - Minor Collection"
echo "python main.py --mode nikaya --nikaya khuddaka --raw --batch-size 100 --delay 1.0"
echo ""

echo "# 5. Scrape අංගුත්තර නිකාය (Aṅguttara Nikāya) - Numerical Discourses"
echo "python main.py --mode nikaya --nikaya anguttara --raw --batch-size 100 --delay 1.0"
echo ""

echo "📁 OUTPUT STRUCTURE:"
echo "output/raw_nikayas/"
echo "├── digha/         # දීඝ නිකාය batches"
echo "├── majjhima/      # මජ්ඣිම නිකාය batches"
echo "├── samyutta/      # සංයුත්ත නිකාය batches"
echo "├── khuddaka/      # ඛුද්දක නිකාය batches"
echo "└── anguttara/     # අංගුත්තර නිකාය batches"
echo ""

echo "⚡ RECOMMENDED ORDER:"
echo "Start with smallest to largest:"
echo "samyutta → digha → majjhima → khuddaka → anguttara"
echo ""

echo "⚠️  IMPORTANT NOTES:"
echo "- Each command scrapes ONE complete Nikaya"
echo "- Uses --raw mode (captures ALL content, no filtering)"  
echo "- Data cleaning will be done in separate stage"
echo "- Can resume if interrupted (progress is saved)"
echo "- Be patient - large Nikayas take several hours"

# Make the script executable
chmod +x "$0"