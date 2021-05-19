import os
import qrcode
import uuid

total_amount = 0

def total(price,quantity):
    ''' helper function to calculate prices '''
    global total_amount
    revenue = float(price)*int(quantity)
    total_amount += revenue
    return format(revenue, '.2f')

def create_pdf(qrcode, table_data):
    ''' 
        qrcode -> the qrcode image filename
        table_data -> list of product details
    '''
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4, portrait

    from reportlab.lib.enums import TA_JUSTIFY

    from reportlab.platypus import SimpleDocTemplate, Spacer, Image, Table
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors

    doc = SimpleDocTemplate(f"{os.path.splitext(qrcode)[0]}.pdf",pagesize=portrait(A4),
                            rightMargin=72,leftMargin=72,
                            topMargin=72,bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))

    Story=[]
    logo = qrcode

    im = Image(logo, 3*inch, 3*inch)
    Story.append(im)

    table_style = [('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')]
    report_table = Table(data=table_data, style=table_style, hAlign="CENTER")
    empty_line = Spacer(1,20)
    
    Story.append(empty_line)
    Story.append(report_table)
    Story.append(empty_line)

    doc.build(Story)

    return doc.filename

def product(data):
    '''
        data is a dict containing customer information and a list with key `product_detail`. we look at each product and append product information to the table_data list.
    '''
    global total_amount

    table_data = [["Sl. No", "Item", "QTY", "Unit Price", "Total"]]
    img = qrcode.make((data['name'], data['phone'], data['email']))
    img_name = f'{uuid.uuid4()}.png'
    img.save(img_name)

    for sl,item in enumerate(data['product_detail']):
        table_data.append([sl+1, item["product_name"], item["quantity"], item["unit_price"],total(item["unit_price"],item["quantity"])])

    # last row for showing the sum of all totals
    table_data.append(['','','','Total Amount:',format(total_amount,'.2f')])
    total_amount = 0
    return create_pdf(img_name, table_data)
    
