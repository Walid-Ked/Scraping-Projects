import scrapy
from itemloaders.processors import Compose, TakeFirst

# A helper function to clean the specifications, 
# Each specification is in the format: <B> .... :</B> and somtimes <B> .... </B> :
# We need to clean it and store the key and value for each spec.

def clean_specs(specs):
    specs_dict = {}
    for spec in specs:
        spec_name = spec.split("</B>")[0][3:].replace(":","")
        spec_value = spec.split("</B>")[1].replace(":","")
        specs_dict[spec_name] = spec_value
    return specs_dict

# Declaration of an Item
class UpshelfItem(scrapy.Item):
    title = scrapy.Field(output_processor = TakeFirst())
    description = scrapy.Field(output_processor = TakeFirst())
    highlights = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field(output_processor = TakeFirst())
    specifications = scrapy.Field(input_processor=Compose(clean_specs), output_processor = TakeFirst())
    questions = scrapy.Field()
    
    