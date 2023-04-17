import traceback

import telebot
import json
from datetime import datetime
import time
import psycopg2

bot = telebot.TeleBot('5430244780:AAHj9xAa2joLUFDUYr_isr54jF8PlMzoIJc')


hostname = 'localhost'
database = 'cobaskripsi'
username = 'postgres'
pwd = '123456'
port_id = 5432
# conn = None
# cur = None

conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id)
cur = conn.cursor()

select_script = '''
            SELECT datastore.tanggal_serang, datastore.waktu_serang FROM datastore
            ORDER BY datastore.tanggal_serang DESC, datastore.waktu_serang DESC'''
try:
    cur.execute(select_script)
    lastdate = cur.fetchone()
except Exception as e:
    print(e)
# print(lastdate)

waktu_sekarang = datetime.now()

timeformat = datetime.strptime(lastdate[0]+' '+lastdate[1], "%Y-%m-%d %H:%M:%S")
timeformat2 = datetime.strftime(timeformat, "%m/%d-%H:%M:%S.%f")
timeformat3 = (str(waktu_sekarang.year) +"/" + timeformat2)
# timeformat3 = "2023/" + timeformat2
lastdatelog = timeformat3
# print(lastdatelog)


# var23 = "gatau"
# delete_script = '''
# 			DELETE FROM datastore
# 			WHERE datastore.jenis_serang = %s'''
# try:
# 	cur.execute(delete_script, (var23, ))
# 	conn.commit()
# except Exception as e:
# 	print(e)

def generateTableIfNotExists():
    # Create Table
    create_script = ''' CREATE TABLE IF NOT EXISTS datastore (
                                id      int PRIMARY KEY,
                                jenis_serang varchar(50) NOT NULL,
                                ip_penyerang varchar(15),
                                ip_diserang varchar(15),
                                port_penyerang varchar(15),
                                port_diserang varchar(15),
                                tanggal_serang varchar(15),
                                waktu_serang varchar(15))'''

    cur.execute(create_script)
    conn.commit()

    # Create Sequence for Auto Increment ID
    seq_script = ''' CREATE SEQUENCE public.autoinc 
    INCREMENT 1
    START 1
    MINVALUE 1; '''
    cur.execute(seq_script)
    conn.commit()

    # Alter table and add sequence
    alter_script = "ALTER TABLE ONLY datastore ALTER COLUMN id SET DEFAULT nextval('autoinc'::regclass);"
    cur.execute(alter_script)
    conn.commit()


# @bot.message_handler(commands=['start'])
# def welcome(message):
#     # membalas pesan
#     # createjson(message)
#     bot.reply_to(message, 'Halo bro, ada apa?')

@bot.message_handler(commands=['list'])
def list(message):
        try:
            textMessage = "Berikut Ini Merupakan Daftar Perintah yang Dapat Digunakan :\n\n" \
                          "1. Input : /logging \nfungsi = menampilkan traffic terkini\n\n" \
                          "2. Input : /reportharian (YYYY-MM-DD) \nfungsi = untuk menampilkan laporan harian berdasarkan format tanggal\n\n" \
                          "3. Input : /reportbulanan (MM) \nfungsi = untuk menampilkan laporan bulanan \n\n" \
                          "4. Input : /totalserangan \nfungsi = untuk menampilkan jumlah total data serangan\n\n" \
                          "5. Input : /jenisserangan (masukkanjenisserangan) \nfungsi = untuk menampilkan jumlah serangan berdasarkan jenis serangan\n\n" \
                          "6. Input : /ippenyerang (masukkan ip penyerang) ) \nfungsi = untuk menampilkan jumlah serangan berdasarkan ip penyerang\n\n" \
                          "7. Input : /ipdiserang (masukkan ip target) \nfungsi = untuk menampilkan jumlah serangan berdasarkan ip yang diserang\n\n" \
                          "8. Input : /portpenyerang (masukkan port penyerang) \nfungsi = untuk menampilkan jumlah serangan berdasarkan port penyerang\n\n" \
                          "9. Input : /portdiserang (masukkan port target) \nfungsi = untuk menampilkan jumlah serangan berdasarkan port yang diserang\n\n"
            chatid = message.chat.id
            bot.send_message(chatid, textMessage)
        except:
            pass

@bot.message_handler(commands=['reportharian'])
def reportharian(message):

    try:
        teks = message.text.split(' ')
        reportharian = teks[1]
        cur.execute("SELECT COUNT (id) FROM datastore WHERE datastore.tanggal_serang = '{}'".format(reportharian))
        totalreportharian = cur.fetchall()
        # print(totalreportharian)
        reply_frombot = ''
        for x in totalreportharian:
            reply_frombot = reply_frombot + "Total Serangan Harian : " +str(x) + '\n'

        reply_frombot = reply_frombot.replace("(", "")
        reply_frombot = reply_frombot.replace(")", "")
        reply_frombot = reply_frombot.replace(",", "")

        bot.reply_to(message, reply_frombot)
    except:
        pass

@bot.message_handler(commands=['reportbulanan'])
def coba(message):

    try:
        select_script = '''
                    SELECT jenis_serang, tanggal_serang FROM datastore'''
        cur.execute(select_script)
        data = cur.fetchall()
        # print(data)

        pesan = message.text.split(' ')
        ambil_pesan = pesan[1]
        # print(ambil_pesan)
        total = 0
        jenser = ""
        ajenser = []
        totaljenser = {}
        detailserang = ""
        # print(total)
        # print(len(data))
        for i in range(len(data)):
            pisah = ' '.join(data[i]).replace('-', ' ').split()
            # print(pisah)
            ambil_bulan = pisah[len(pisah)-2]
            # print(ambil_bulan)
            # msg = pisah[0], pisah[1]
            # print(msg)
            # print(ambil_bulan)

            for index, p in enumerate(pisah):
                if ambil_bulan == ambil_pesan:
                    if index == (len(pisah) - 4):
                        jenser += p
                        continue
                    elif index < (len(pisah) - 3):
                        jenser += p + " "
                        continue
                    else:
                        if jenser not in ajenser:
                            ajenser.append(jenser)
                        for tipe in ajenser:
                            if jenser == tipe:
                                if jenser in totaljenser:
                                    totaljenser[tipe] += 1
                                else:
                                    totaljenser[tipe] = 1
                            else:
                                continue
                        jenser = ""
                        break

            # print(total)
            if ambil_bulan == ambil_pesan:
                total += 1
                continue
            else:
                continue


            # select_script2 = ''' SELECT jenis_serang, COUNT(jenis_serang) AS JumlahSerangan FROM datastore GROUP BY (jenis_serang) '''
            # cur.execute(select_script2)
            # databaru = cur.fetchall()
            # print(databaru)
            # for i in range(len(databaru)):
            #
            #     pisah = ' '.join(data[i])
            # print(pisah)
            # print(total)

        for value in totaljenser:
            # print(totaljenser[value])
            if detailserang == {}:
                detailserang = value + " : " + str(totaljenser[value]) + "\n"
                continue
            else:
                detailserang += value + " : " + str(totaljenser[value]) + "\n"
                continue

        # print(detailserang)
        reply_frombot = "Total Serangan Bulanan : " + str(total) + '\n\n' \
                                                                   'Berikut Ini Merupakan Rincian Dari Serangan : \n' + detailserang + '\n*note : Rincian Berdasarkan Jenis Serangan dan Jumlah Serangan'

        bot.reply_to(message, reply_frombot)
    except:
        pass

# @bot.message_handler(commands=['reportbulanan'])
# def reportbulanan(message):
#
#     try:
#         select_script = '''
#                     SELECT tanggal_serang FROM datastore
#                     ORDER BY datastore.tanggal_serang ASC'''
#         cur.execute(select_script)
#         banyak_tanggal = cur.fetchall()
#         # print(banyak_tanggal)
#         pesan = message.text.split(' ')
#         # print(pesan)
#         total = 0
#         # print(total)
#         # print(len(banyak_tanggal))
#         for i in range(len(banyak_tanggal)):
#             tanggal = ' '.join(banyak_tanggal[i]).replace('-', ' ').split()
#             # print(tanggal)
#             bulan = tanggal[1]
#             # print(bulan)
#
#             # print(total)
#             if bulan == pesan[1]:
#                 total += 1
#                 continue
#             else:
#                 continue
#
#         # print(total)
#         reply_frombot = "Total Serangan Bulanan : " + str(total) + '\n'
#         # reportbulanan =
#
#         # cur.execute("SELECT COUNT (id) FROM datastore WHERE datastore.tanggal_serang = '{}'".format(reportbulanan))
#         # totalreportbulanan = cur.fetchall()
#         # # print(totalreportharian)
#
#         # reply_frombot = ''
#         # for x in total:
#         #     reply_frombot = reply_frombot + "Total Serangan Bulanan : " +str(x) + '\n'
#         #
#         # reply_frombot = reply_frombot.replace("(", "")
#         # reply_frombot = reply_frombot.replace(")", "")
#         # reply_frombot = reply_frombot.replace(",", "")
#
#         bot.reply_to(message, reply_frombot)
#     except:
#         pass

@bot.message_handler(commands=['totalserangan'])
def totalserangan(message):

    try:
        cur.execute("SELECT COUNT (id) FROM datastore")
        totalserangan = cur.fetchall()
        # print(totalserangan)
        reply_frombot = ''
        for x in totalserangan:
            reply_frombot = reply_frombot + "Total Keseluruhan Serangan : " +str(x) + '\n'

        reply_frombot = reply_frombot.replace("(", "")
        reply_frombot = reply_frombot.replace(")", "")
        reply_frombot = reply_frombot.replace(",", "")

        bot.reply_to(message, reply_frombot)
    except:
        pass

@bot.message_handler(commands=['jenisserangan'])
def jenisserangan(message):
    selectjenisserang_script = '''
                            SELECT jenis_serang FROM datastore
                            '''
    cur.execute(selectjenisserang_script)
    jenisserangpertama = cur.fetchall()
    # # pengganti = ''
    # for x in jenisserangpertama:
    #
    # jenisserangpertama = jenisserangpertama.re(" ","")
    # print("".join(jenisserangpertama()))
    # print(jenisserangpertama)
    try:
        teks = message.text.split(' ')
        # jenis_serang = teks[1]
        if len(teks) > 2:
            for index, jenis in enumerate(teks):
                if index == 0:
                    continue
                else:
                    if index == 1:
                        jenis_serang = str(jenis) + ' '
                        # print(jenis_serang)
                    elif index + 1 == len(teks):

                        jenis_serang = jenis_serang + str(jenis)
                        # print(jenis_serang)
                    else:
                        jenis_serang = jenis_serang + str(jenis) + ' '
                        # print(jenis_serang)
        else:
            jenis_serang = teks[1]
        # print(jenis_serang)
        select = " SELECT COUNT (id) FROM datastore WHERE jenis_serang = '"+str(jenis_serang)+"'"
        cur.execute(select)
        jenisserangan = cur.fetchall()
        # print(jenisserangan)
        reply_frombot = ''
        for x in jenisserangan:
            reply_frombot = reply_frombot + "Total Keseluruhan Jenis Serangan : " +str(x) + '\n'

        reply_frombot = reply_frombot.replace("(", "")
        reply_frombot = reply_frombot.replace(")", "")
        reply_frombot = reply_frombot.replace(",", "")

        bot.reply_to(message, reply_frombot)
    except:
        pass

@bot.message_handler(commands=['ippenyerang'])
def ippenyerang(message):

    try:
        teks = message.text.split(' ')
        ip_penyerang = teks[1]
        cur.execute("SELECT COUNT (id) FROM datastore WHERE ip_penyerang = '{}'".format(ip_penyerang))
        hasilipp = cur.fetchall()
        # print(hasilipp)
        reply_frombot = ''
        for x in hasilipp:
            reply_frombot = reply_frombot + "IP Terdeteksi Melakukan : " +str(x) + "x Penyerangan" + '\n'

        reply_frombot = reply_frombot.replace("(", "")
        reply_frombot = reply_frombot.replace(")", "")
        reply_frombot = reply_frombot.replace(",", "")

        bot.reply_to(message, reply_frombot)
    except:
        pass

@bot.message_handler(commands=['ipdiserang'])
def ipdiserang(message):

    try:
        teks = message.text.split(' ')
        ip_diserang = teks[1]
        cur.execute("SELECT COUNT (id) FROM datastore WHERE ip_diserang = '{}'".format(ip_diserang))
        hasilipd = cur.fetchall()
        # print(hasilipd)
        reply_frombot = ''
        for x in hasilipd:
            reply_frombot = reply_frombot + "IP Terdeteksi Sebanyak : " +str(x) +"x Diserang"+'\n'

        reply_frombot = reply_frombot.replace("(", "")
        reply_frombot = reply_frombot.replace(")", "")
        reply_frombot = reply_frombot.replace(",", "")

        bot.reply_to(message, reply_frombot)
    except:
        pass

@bot.message_handler(commands=['portpenyerang'])
def portpenyerang(message):

    try:

        teks = message.text.split(' ')
        port_penyerang = teks[1]
        cur.execute("SELECT COUNT (id) FROM datastore WHERE port_penyerang = '{}'".format(port_penyerang))
        hasilportp = cur.fetchall()
        # print(hasilportp)
        reply_frombot = ''
        for x in hasilportp:
            reply_frombot = reply_frombot + "Port Penyerang Terdeteksi Sebanyak : " +str(x) +"x"+ '\n'

        reply_frombot = reply_frombot.replace("(", "")
        reply_frombot = reply_frombot.replace(")", "")
        reply_frombot = reply_frombot.replace(",", "")

        bot.reply_to(message, reply_frombot)
    except:
        pass

@bot.message_handler(commands=['portdiserang'])
def portdiserang(message):

    try:
        teks = message.text.split(' ')
        port_diserang = teks[1]
        cur.execute("SELECT COUNT (id) FROM datastore WHERE port_diserang = '{}'".format(port_diserang))
        hasilportd = cur.fetchall()
        # print(hasilportd)
        reply_frombot = ''
        for x in hasilportd:
            reply_frombot = reply_frombot + "Port Diserang Terdeteksi Sebanyak : " +str(x) +"x"+ '\n'

        reply_frombot = reply_frombot.replace("(", "")
        reply_frombot = reply_frombot.replace(")", "")
        reply_frombot = reply_frombot.replace(",", "")

        bot.reply_to(message, reply_frombot)
    except:
        pass

@bot.message_handler(commands=['logging'])
def logging(message):
    while True:
        try:
            time.sleep(10)
            print("send log")
            data = createjson(message)
            if data == 0:
                break
        except:
            pass

def createjson(message):
    global lastdatelog
    # waktu_sekarang = datetime.now()
    # print(waktu_sekarang.year)
    # Opening JSON file
    f = open('alert_json.txt')
    pecah = f.read().split("}")
    # print(pecah)
    json_format = "["

    for index, i in enumerate(pecah):
        json_format += i
        if index >= len(pecah) - 2:
            pass
        else:
            json_format += "}, "

    json_format += "}]"

    # print(json_format)
    # returns JSON object as
    # a dictionary
    data = json.loads(json_format)
    # print(data)
    # json.x
    # data = json.dumps(json_format, sort_keys=True, indent=2, separators=(',', ': '))

    # Iterating through the json
    # list
    for index, i in enumerate(data):
        # @bot.message_handler(commands=['berhenti'])
        # try:
        #     stop = berhenti()
        #     return stop
        # except:
        #     traceback.print_exc()

        # log_timestamp = i['timestamp'] + " 2022"
        # if 'msgs' in i:
        #     print('testt')
        # else:
        #     print('x')

        # log_timestamp = "2022/" + i['timestamp']
        snort_timestamp = (str(waktu_sekarang.year) +"/" + i['timestamp']) if 'timestamp' in i else None
        # print(log_timestamp)
        # print(i['dst_port'])
        # print(i['src_port'])
        # print(f"Port: {data['dst_port']}")
        jenis = i['msg'] if 'msg' in i else None
        # print(jenis)
        port1 = str(i['src_port']) if 'src_port' in i else None
        port2 = str(i['dst_port']) if 'dst_port' in i else None
        ip1 = i['src_addr'] if 'src_addr' in i else None
        ip2 = i['dst_addr'] if 'dst_addr' in i else None
        # print(port1)
        # print(port2)
        # converted_port = str(port)

        # print(snort_timestamp+"/")

        last_datetime = datetime.strptime(lastdatelog, "%Y/%m/%d-%H:%M:%S.%f")
        log_datetime = datetime.strptime(snort_timestamp, "%Y/%m/%d-%H:%M:%S.%f")
        # print(last_datetime)
        # print(log_datetime)
        tanggal = log_datetime.strftime("%Y-%m-%d")
        waktu = log_datetime.strftime("%H:%M:%S")

        # print(tanggal)
        # print(waktu)
        # cetak_waktu = datetime.strptime(log_timestamp, "%H:%M:%S")
        #
        # print(last_datetime.date())
        # print(log_datetime.date())
        #
        # difference = log_datetime - last_datetime
        # print(difference)
        # print(difference.)
        #
        if log_datetime > last_datetime:
            # print("true")
            # print(log_datetime)
            # print("log_datetime > last_datetime:")
            # bot.reply_to(message, i['src_addr'])
            textMessage = ""

            if jenis is not None:
                textMessage += "Jenis Serangan : " + jenis
            if ip1 is not None:
                textMessage += "\nIP Penyerang : " + ip1
            if ip2 is not None:
                textMessage += "\nIP Diserang : " + ip2
            if port1 is not None:
                textMessage += "\nPort Penyerang : " + port1
            if port2 is not None:
                textMessage += "\nPort Diserang : " + port2
            if tanggal is not None:
                textMessage += "\nTanggal Serang : " + tanggal
            if waktu is not None:
                textMessage += "\nWaktu Serang : " + waktu

            chatid = message.chat.id
            bot.send_message(chatid, textMessage)
            # print(jenis, ip1, ip2, port1, port2, tanggal, waktu)

            insertToDB(jenis, ip1, ip2, port1, port2, tanggal, waktu)

            if index == len(data) -1 :
                return 0

            # bot.send_message(chatid, "IP Serangan : " + i['src_addr'])

            # lastdatelog = log_datetime
            # print(lastdatelog)
            # print(last_datetime)
            # Closing file
            f.close()


def insertToDB(jenis, ipp, ips, pp, ps, tanggal, waktu):
    insert_script = '''
                        INSERT INTO datastore
                        (jenis_serang, ip_penyerang, ip_diserang, port_penyerang, port_diserang,
                        tanggal_serang, waktu_serang)
                        VALUES ( %s, %s, %s, %s, %s, %s, %s)'''
    insert_values = (jenis, ipp, ips, pp, ps, tanggal, waktu)
    #print(jenis, ipp, ips, pp, ps, tanggal, waktu)
    try:
        cur.execute(insert_script, insert_values)
    except Exception as e:
        print(e)
        pass

    conn.commit()

# insertToDB('gatau', '123121241', '23123123', '80', '443', '12', '23')

while True:
    try:
        bot.polling()
    except:
        pass

# except Exception as error:
#      print(error)
#     finally:
#         if cur is not None:
#             cur.close()
#         if conn is not None:
#             conn.close()
# createjson()
# generateTableIfNotExists()
# depa
