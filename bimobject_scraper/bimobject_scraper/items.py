from scrapy import Item, Field
from itemloaders.processors import MapCompose, TakeFirst
from typing import Optional, Any


def strip_string(x: Any) -> Optional[str]:
    """
    Препроцессинг строки
    """
    return str(x).strip() if x is not None else x


class BimobjectScraperItem(Item):
    url = Field(
        input_processor=MapCompose(strip_string),
        output_processor=TakeFirst()
    )
    categories = Field(
        input_processor=MapCompose(strip_string)
    )
    title = Field(
        input_processor=MapCompose(strip_string),
        output_processor=TakeFirst()
    )
    title_rus = Field()
    omni_code = Field(
        input_processor=MapCompose(strip_string),
        output_processor=TakeFirst()
    )
    omni_class_name = Field(
        input_processor=MapCompose(strip_string),
        output_processor=TakeFirst()
    )
    omni_class_name_rus = Field()
