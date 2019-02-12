import os
import yaml
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth 
from reportlab.lib.utils import ImageReader

MARGIN = 40
INDENT = 10
MARGIN_SECTION = 25
SECTION_ICON_SIZE = 14
DOCUMENTS_NAME = {
    'fr': 'output/CV', 
    'en': 'output/resume'
}
SECTIONS_NAME = {
    'fr' : {
        'summary': 'Sommaire',
        'skills' : 'Compétences',
        'experiences': 'Parcours professionnel',
        'more_informations': "Plus d'informations"
    },
    'en' : {
        'summary': 'Summary',
        'skills' : 'Skills',
        'experiences': 'Experiences',
        'more_informations': "More informations"
    },
}
SECTIONS_IMAGES = {
    'summary' : 'images/book.png',
    'skills' : 'images/black_star.png',
    'experiences': 'images/wired_keyboard.png',
    'more_informations': 'images/more_information.png'
}
PROFILE_PICTURE = 'images/profile_picture.png'
PROFILE_PICTURE_X = 25

class CVBuilder:
    def __init__(self, filename, language):
        self.canvas = canvas.Canvas(filename, pagesize=letter)
        self.width, self.height = letter
        self.y = self.height - MARGIN
        self.language = language

    def set_font(function):
        def set_font_decorator(self):
            font, font_size = function(self)  # run decorated function
            self.font = font
            self.font_size = font_size
            self.canvas.setFont(self.font, self.font_size)
        return set_font_decorator

    @set_font
    def set_font_name(self):
        return 'Times-Bold', 17

    @set_font
    def set_font_title(self):
        return 'Times-Bold', 17

    @set_font
    def set_font_contact_information(self):
        return 'Times-Roman', 10
    
    @set_font
    def set_font_section(self):
        return 'Times-Bold', 14

    @set_font
    def set_font_summary(self):
        return 'Times-Roman', 10

    @set_font
    def set_font_normal(self):
        return 'Times-Roman', 10

    @set_font
    def set_font_normal_bold(self):
        return 'Times-Bold', 10

    @set_font
    def set_font_small(self):
        return 'Times-Roman', 9

    def add_section(self, section_name):
        self.y -= MARGIN_SECTION
        self.canvas.setFillColorRGB(0.37, 0.49, 0.54) 
        self.canvas.rect(MARGIN - 15 , cv.y-5, cv.width - 2 * MARGIN, cv.font_size + 7, stroke=0, fill=1)
        self.canvas.setStrokeColorRGB(1,1,1) 
        self.canvas.circle(MARGIN * 3, cv.y + 4, cv.font_size+3, stroke=1, fill=1)
        self.canvas.setFillColorRGB(1,1,1) 
        self.canvas.circle(MARGIN * 3, cv.y + 4, cv.font_size+1, stroke=1, fill=1)
        logo = ImageReader(SECTIONS_IMAGES[section_name])

        self.canvas.drawImage(logo, MARGIN * 3 - SECTION_ICON_SIZE/2, cv.y + 4 - SECTION_ICON_SIZE/2, mask='auto', width=SECTION_ICON_SIZE, height=SECTION_ICON_SIZE)
        
        self.canvas.setFillColorRGB(1, 1, 1) 
        self.set_font_section()
        self.draw_text(SECTIONS_NAME[self.language][section_name], indent = 12)

        self.y -= MARGIN_SECTION / 4
        self.canvas.setFillColorRGB(0, 0, 0) 

    def draw_text(self, text, alignement = 'left', indent = 0):
        text = text.strip()
        x = MARGIN + INDENT * indent
        total_text_width = stringWidth(text, self.font, self.font_size)
        max_text_width = self.width - x - MARGIN
        next_text = False
        if total_text_width > max_text_width:
            words = text.split(' ')
            writable_text = ""
            for i, word in enumerate(words):
                writable_text += f"{word} "
                if stringWidth(writable_text, self.font, self.font_size) < max_text_width:
                    text = writable_text
                else:
                    next_text = ' '.join(words[i:])
                    break
        if alignement == 'center':
            x = (self.width - total_text_width) / 2
        if alignement == 'right':
            x = self.width - total_text_width - MARGIN * 2 - INDENT * indent
        self.canvas.drawString(x, self.y, text)
        self.y -= self.font_size
        if next_text:
            self.draw_text(next_text, indent=indent)

    def save(self):
        self.canvas.save()

if __name__ == '__main__':

    for file in os.scandir('.'):
        if file.name.endswith('.yml'):
            for language in ['fr', 'en']:
                cv_filename = DOCUMENTS_NAME[language]
                cv = CVBuilder(cv_filename, language)
                with open(file.name, 'r') as f:
                    cv_data = yaml.load(f.read())['cv']
                    
                    # Name
                    cv.set_font_name()
                    cv.canvas.setFillColorRGB(0.37, 0.49, 0.54) 
                    cv.canvas.rect(0, cv.y-8, cv.width, cv.font_size + 8, stroke=0, fill=1)
                    cv.canvas.setFillColorRGB(1, 1, 1) 
                    cv.draw_text(f"{cv_data['personnal_informations']['first_name']} {cv_data['personnal_informations']['last_name']}", "center")
                    cv.canvas.setFillColorRGB(0, 0, 0) 
                    cv.y -= 10

                    # Title
                    cv.set_font_title()
                    cv.draw_text(cv_data['title'][language], "center")

                    # Profile picture
                    profile_picture = ImageReader(PROFILE_PICTURE)
                    cv.canvas.drawImage(profile_picture, PROFILE_PICTURE_X, cv.y - 20, mask='auto', width=100, height=100)

                    # Contact information
                    cv.set_font_contact_information()
                    contact_informations = []
                    if 'address' in cv_data['personnal_informations']:
                        contact_informations.append(', '.join(cv_data['personnal_informations']['address']))
                    if 'phone' in cv_data['personnal_informations']:
                        contact_informations.append(cv_data['personnal_informations']['phone'])
                    if 'mail' in cv_data['personnal_informations']:
                        contact_informations.append(cv_data['personnal_informations']['mail'])

                    cv.draw_text(' | '.join(contact_informations), "center")

                    cv.y -= 20

                    # Summary
                    cv.add_section('summary')
                    cv.set_font_summary()
                    for line in cv_data['summary'][language]:
                        cv.draw_text(line)

                    # Skills
                    cv.add_section('skills')
                    cv.set_font_normal()
                    for skill, attributes in cv_data['skills'].items():
                        cv.set_font_normal_bold()
                        cv.draw_text(skill.strip())
                        cv.set_font_normal()
                        if 'level' in attributes:
                            # Skill bar
                            cv.canvas.setFillColorRGB(0.59, 0.86, 0.58)
                            cv.canvas.rect(170, cv.y + cv.font_size, 50, cv.font_size - 4, stroke=0, fill=1)
                            cv.canvas.setFillColorRGB(0.187, 0.597, 0.18)
                            cv.canvas.rect(170, cv.y + cv.font_size, 10 * attributes['level'], cv.font_size - 4, stroke=0, fill=1)
                            
                        cv.canvas.setFillColorRGB(0,0,0)
#                            string += f" {attributes['level']}"
                        if 'subskills' in attributes:
                            cv.y += cv.font_size # get back on above line
                            subskills = f"{', '.join(attributes['subskills'])}"
                            cv.set_font_small()
                            cv.draw_text(subskills, indent=20)

                    # Experiences
                    cv.add_section('experiences')
                    for company, attributes in cv_data['experiences'].items():
                        cv.set_font_normal()
                        cv.draw_text(f"{attributes['start']} - {attributes['end']}")
                        cv.set_font_normal_bold()
                        cv.y += cv.font_size  # get back one above line
                        cv.draw_text(company.strip(), indent=15)
                        cv.set_font_normal()
                        cv.draw_text(attributes[f'summary_{language}'], indent = 1)
                        cv.draw_text("")

                    # More
                    cv.add_section('more_informations')
                    for line in cv_data['more'][language]:
                        cv.set_font_normal()
                        cv.draw_text(line)
                cv.save()
