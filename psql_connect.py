import psycopg2


def populate_address_table():
    connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    cursor = connection.cursor()
    cursor.execute("SELECT street_address, span FROM public.rental_compliance;")
    span_address_row = cursor.fetchall()
    for  span_address in span_address_row:
        if( '-' in span_address[0]):
            print(span_address[0])
            address_split = span_address[0].split(' ')
            address_range = address_split[0].split('-')
            lower_bound = int(address_range[0])
            upper_bound = int(address_range[1])
            for i in range(lower_bound, upper_bound+1):
                apt_number = str(i)
                span_number = span_address[1]
                address = apt_number + " " + address_split[1] + " " + address_split[2]
                row = (str(span_number), str(address))
                cursor.execute("INSERT INTO address_span VALUES (%s, %s);", row)
        else:
            address = span_address[0]
            span_number = span_address[1]
            row = (str(span_number), str(address))
            print(address)
            cursor.execute("INSERT INTO address_span VALUES (%s, %s);", row)
    connection.commit()


def create_address_table():
    connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    cursor2 = connection.cursor()
    cursor2.execute("CREATE TABLE address_span(span TEXT, street_address TEXT)")
    connection.commit()


def get_span():
    spans = []
    connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    cursor = connection.cursor()
    cursor.execute("SELECT span FROM public.rental_comp;")
    span_row = cursor.fetchall()
    counter = 0
    for  span in span_row:
        if(counter != 2111):
            span_num = span[0].split('-')
            last = span_num[2]
            # print(str(counter) + " " + last)
            counter += 1
            number = int(last)
            spans.append(number)
    spans.sort()
    for i in range(0, len(spans)-1):
        if(spans[i]== spans[i+1]):
            print(spans[i])
    # for s in spans:
    #     if()
    #     print(s)


def main():
    # connection = psycopg2.connect(host="localhost", database="btvignite", user="clasbychope", password="burlington")
    # cursor = connection.cursor()
    # cursor.execute("SELECT * FROM public.rental_compliance;")
    # rows = cursor.fetchall()
    # for row in rows:
    #     print(row)
    # connection.close()

    # only needs to be run once
    # create_address_table()
    # populate_address_table()

    get_span()


main()
