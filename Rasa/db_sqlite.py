import sqlite3
import contextlib

def insert_data(isim, number, date, randevu_not):
    with contextlib.closing(sqlite3.connect('veri.db')) as conn:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                #tablonun veri tabanında olup olmadığını kontrol edilmesi
                cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='hastalar' ''')

                #tablo sayısı 1'den farklı ise tablo daha yaratılmamış demektir
                if cursor.fetchone()[0]==0 : 
                    sql = ''' CREATE TABLE IF NOT EXISTS hastalar(isim VARCHAR, number VARCHAR, date VARCHAR, randevu_not VARCHAR) '''
                    cursor.execute(sql)
                    conn.commit()
                try:
                    cursor.execute('''INSERT INTO hastalar(isim, number, date, randevu_not) VALUES (?, ?, ?, ?)''', (isim, number, date, randevu_not))
                    conn.commit()
                    return f"Randevunuz başarılı bir şekilde kaydedilmiştir. Size yardımcı olabileceğim başka konu var mı?"
                except:
                    return f"Randevunuz kaydedilememiştir. Lütfen daha sonra yeniden deneyiniz. Bu sorunu almaya devam ederseniz bize telefondan ulaşabilirsiniz. Size yardımcı olabileceğim başka konu var mı?"

def get_data(number):
    with contextlib.closing(sqlite3.connect('veri.db')) as conn:
        with conn:
            with contextlib.closing(conn.cursor()) as cursor:
                #tablonun veri tabanında olup olmadığını kontrol edilmesi
                cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='hastalar' ''')
                #tablo sayısı 1'den farklı ise tablo daha yaratılmamış demektir
                if cursor.fetchone()[0]!=0 :
                    if number.isdigit():
                        query = ''' SELECT * FROM hastalar WHERE number={0} '''.format(number)
                        cursor.execute(query)
                        conn.commit()
                        rows = cursor.fetchall()
                        if len(rows) == 0:
                            return f"Adınıza randevu görünmüyor. Size yardımcı olabileceğim başka konu var mı?"
                        else:
                            bilgiler = ['İsim', 'Numara', 'Tarih', 'Notlar']
                            randevu_bilgisi = ""
                            for row in rows:
                                for i, bilgi in enumerate(row):
                                    randevu_bilgisi += bilgiler[i] + ":" + bilgi + "\n"
                            return f"Randevu bilgileriniz\n" + randevu_bilgisi + "\nSize yardımcı olabileceğim başka konu var mı?"
                    else:
                        return f"Randevu kaydınıza ulaşamadım. Size başka nasıl yardımcı olabilirim?"
                else: 
                    return f"Randevu kaydınıza ulaşamadım. Size yardımcı olabileceğim başka konu var mı?"