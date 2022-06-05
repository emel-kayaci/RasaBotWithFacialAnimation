# Tıp Alanında Doğal Dil İşleme Destekli Dijital İkiz Tasarımı (GBYF Yarışması Eğitim, Eğlence ve Oyun kategorisi Ege Bölgesi 1.si)

Projemizde gerçek yüz (meslek dallarında önemli kişiler veya kahramanlar vb.) içeren hareketli bir görsel aracılığı ile yapay zekanın ürettiği söylemleri mimikleri, dudak hareketleri ve ses ile karşıya aktarmayı sağlayan derin öğrenme tabanlı bir sistem geliştirilmiştir.

Kullanıcıya yalnızca metinsel dönüt vermek yerine bu dönütün gerçek bir insan yüzüyle de desteklenmesi, konuşmanın çok daha etkileyici ve motive edici olmasını sağlamıştır.

https://user-images.githubusercontent.com/43893190/170813959-396104be-e9fe-434f-978d-08cf0cd02cd2.mp4

## Özgün Değer

- Yaşayan bir kimsenin mesleki bilgisi ile konuşma tarzı ve görüntüsünün bir arada verilmesi yönü ile yenilikçidir.
 
- Türkçe olarak hiçbir yerde bulunmayan hastalık ve semptomlar için bir veri seti hazırlanmıştır. 

- RASA kütüphanesinde doğal dil işleme mekanizmasının akışı (pipeline) tamamen Türkçe verilere özgü tasarlanmıştır.

- Doğal dil işleme ve yüz canlandırma modülleri web üzerinde entegre edilerek, gerçek zamanlı veri akışı sağlanmıştır. 

## Uygulanabilirlik

- Proje, uygun metinsel ve görsel veriler sağlanırsa sağlık alanı dışında turizm, eğitim, muhasebe ve finans gibi alanlarda da kullanılabilir.  

- Ek bir maliyet gerektirmeden yalnızca canlandırılması istenilen kişiye ait tek bir görüntü ile farklı kişilerin yüzlerine uyarlanabilecek bir yapıdadır.  

- Proje evrensel olup her dile uyarlanabilir. 

## Yöntem

<img src="https://user-images.githubusercontent.com/43893190/170813759-ba8e6119-476a-4a0c-a6dc-1ff972292475.PNG" width="750"/>

### Yüz Canlandırma Yöntemi

- Yüz canlandırma modülü, hem RASA teknolojisi hem de Web entegrasyonu ile bağlantılı çalışmakta olup, image2image translation mantığına dayanan ‘MakeItTalk’ mimarisidir. 

- Bu mimari, LSTM (long-short term memory) kullanılarak girdi olarak gelen ses dosyasının, hedef kişide yaptırabileceği yüz hareketlerini tahmin edip, bu tahminleri yüz üzerinde birtakım manipulasyonlar yaparak gerçekleştirmeye dayanır. 

[MakeItTalk](https://github.com/yzhou359/MakeItTalk)

### Doğal Dil İşleme Yöntemi

<img src="https://user-images.githubusercontent.com/43893190/170813850-92fd7403-7aef-4d63-83bf-24df96953f09.PNG" width="750"/>

## Kullanılan Teknolojiler

<img src="https://user-images.githubusercontent.com/43893190/170813870-d4b23617-ea96-45d4-a89a-0f5142ad42a4.PNG" width="750"/>

## Kullanım

Aşağıdaki kodları çalıştırmadan önce lütfen [MakeItTalk](https://github.com/yzhou359/MakeItTalk) kütüphanesini indiriniz.

```python
# Sırasıyla aşağıdaki komutları terminal üzerinden çalıştırın, komutları çalıştırmadan önce 
# virtual env aktive ediniz. 

# Öncelikle rasa modelini aktive ediyoruz
rasa run -m models --enable-api 
# Rasa'da yer alan actions.py dosyasını çalıştırıyoruz
rasa run actions
# Backend tarafında çalışan flask dosyasını çalıştırıyoruz 
python route.py
# Frontend tarafında çalışan kısmı aktive ediyoruz
python -m http.server  
```

## Kullanım Örneği

https://user-images.githubusercontent.com/43893190/170813976-a88f10e5-6623-4284-a3af-5217d69e7bdc.mp4


## Geliştiriciler

[Mehmet Anıl Taysi](https://github.com/MehmetAnil) - aniltaysi@gmail.com

[Emel Kayacı](https://github.com/emel-kayaci) - kayaciemel18@gmail.com
