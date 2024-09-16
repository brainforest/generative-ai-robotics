import re
from num2words import num2words

def convert_numbers_to_words(text):
    """Convert percentages like %3.5 or %90 to their Turkish equivalents."""
    
    # Regular expression to find percentages like %3.5 or %90
    percentage_pattern = re.compile(r'(\d+(\.\d+)?)')
    
    def replace_with_words(match):
        number = match.group(1)
        # Convert the number to Turkish words
        if '.' in number:
            # Handle decimal numbers
            parts = number.split('.')
            integer_part = num2words(int(parts[0]), lang='tr')
            decimal_part = num2words(int(parts[1]), lang='tr')
            return f"{integer_part} virgül {decimal_part}"
        else:
            # Handle whole numbers
            return f"{num2words(int(number), lang='tr')}"
    
    # Replace all percentages in the text with their Turkish equivalents
    return percentage_pattern.sub(replace_with_words, text)

# Example usage
text = "Bu ürün 3.5 kilogram ve fiyatı 90 lira."
converted_text = convert_numbers_to_words(text)
print(converted_text)
