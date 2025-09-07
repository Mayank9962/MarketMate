import os 
import datetime 
import pyttsx3 
 
def generate_pdf_report(data: dict): 
    """ 
    Generates a text report from the analysis data. 
    """ 
    report_date = datetime.date.today().strftime("%Y-%m-%d") 
    filename = f"market_report_{report_date}.txt" 

    # Text content for the report 
    report_content = f""" 
MARKET ANALYSIS REPORT
=====================

Title: {data['title']}
Date: {data['date']}
Product Line: {data['product_line']}

COMPETITOR OVERVIEW
------------------
Top Competitors: {', '.join(data['competitors'])}

REVIEW SUMMARY
-------------
Overall Sentiment: {data['reviews'].get('overall_sentiment', 'N/A')}
Summary: {data['reviews'].get('overall_summary', 'N/A')}

MARKET TRENDS
-------------
{chr(10).join([f"• {t}" for t in data['trends']])}

HISTORICAL COMPARISON
--------------------
Last Week's Data:
• Trends: {', '.join(data['historical_data'].get('trends', ['N/A'])) if data['historical_data'] else 'N/A'}
• Sentiment: {data['historical_data'].get('reviews', {}).get('overall_sentiment', 'N/A') if data['historical_data'] else 'N/A'}

FINAL RECOMMENDATIONS
--------------------
{data['recommendations']}

=====================
Report generated on: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
""" 

    # Write the text report 
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return filename 
 
def generate_voice_summary(text: str): 
    """ 
    Converts text to speech using pyttsx3. 
    """ 
    print("[TTS] -> Starting voice summary...") 
    engine = pyttsx3.init() 
    engine.say(text) 
    engine.runAndWait()