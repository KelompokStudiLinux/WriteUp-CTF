<h1 align="center">Corrupted Disk</h1>

## Description

We've recovered this disk image but it seems to be damaged.
Can you recover any useful information from it?

### File

[recovered_disk.img](./recovered_disk.img)

## Solution

Diberikan file *recovered_disk.img*. <br />
Disini kami mencoba menggunakan **binwalk** untuk memeriksa isi dari file img tersebut.

```
❯ binwalk recovered_disk.img

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
36527         0x8EAF          LZMA compressed data, properties: 0x5E, dictionary size: 0 bytes, uncompressed size: 1012 bytes
1229488       0x12C2B0        PDF document, version: "1.4"
1229559       0x12C2F7        Zlib compressed data, default compression
1229798       0x12C3E6        Zlib compressed data, default compression
1240906       0x12EF4A        Zlib compressed data, default compression
1242800       0x12F6B0        PNG image, 1068 x 966, 8-bit/color RGBA, non-interlaced
1242864       0x12F6F0        Zlib compressed data, best compression
1257302       0x132F56        Zlib compressed data, default compression
2586288       0x2776B0        PNG image, 316 x 20, 8-bit grayscale, non-interlaced
3669680       0x37FEB0        JPEG image data, JFIF standard 1.01
3669710       0x37FECE        TIFF image data, little-endian offset of first image directory: 8
3669972       0x37FFD4        JPEG image data, JFIF standard 1.01
3931824       0x3BFEB0        JPEG image data, EXIF standard
3931836       0x3BFEBC        TIFF image data, little-endian offset of first image directory: 8
4062896       0x3DFEB0        Zip archive data, at least v2.0 to extract, name: _rels/.rels
4063170       0x3DFFC2        Zip archive data, at least v2.0 to extract, name: word/settings.xml
4063419       0x3E00BB        Zip archive data, at least v2.0 to extract, name: word/_rels/document.xml.rels
4063795       0x3E0233        Zip archive data, at least v2.0 to extract, name: word/fontTable.xml
4064209       0x3E03D1        Zip archive data, at least v2.0 to extract, name: word/numbering.xml
4065083       0x3E073B        Zip archive data, at least v2.0 to extract, name: word/media/image1.jpeg
4165523       0x3F8F93        Zip archive data, at least v2.0 to extract, name: word/charts/chart1.xml
4166418       0x3F9312        Zip archive data, at least v2.0 to extract, name: word/styles.xml
4167646       0x3F97DE        Zip archive data, at least v2.0 to extract, name: word/document.xml
4172416       0x3FAA80        Zip archive data, at least v2.0 to extract, name: docProps/app.xml
4172647       0x3FAB67        Zip archive data, at least v2.0 to extract, name: docProps/core.xml
4172993       0x3FACC1        Zip archive data, at least v2.0 to extract, name: [Content_Types].xml
4174177       0x3FB161        End of Zip archive, footer length: 22
```

Terlihat ada banyak sekali file didalamnya. Langsung saja!

```
❯ binwalk --extract recovered_disk.img
```
**binwalk --extract** digunakan untuk mengextract isi dari file tersebut. <br />
Menghasilkan sebuah directory **_recovered_disk.img.extracted**

```
❯ ls -l _recovered_disk.img.extracted
total 18700
-rw-r--r-- 1 x wheel     189 Mar 31 12:27  12C2F7
-rw-r--r-- 1 x wheel 2963385 Mar 31 12:27  12C2F7.zlib
-rw-r--r-- 1 x wheel   23164 Mar 31 12:27  12C3E6
-rw-r--r-- 1 x wheel 2963146 Mar 31 12:27  12C3E6.zlib
-rw-r--r-- 1 x wheel     450 Mar 31 12:27  12EF4A
-rw-r--r-- 1 x wheel 2952038 Mar 31 12:27  12EF4A.zlib
-rw-r--r-- 1 x wheel   25492 Mar 31 12:27  12F6F0
-rw-r--r-- 1 x wheel 2950080 Mar 31 12:27  12F6F0.zlib
-rw-r--r-- 1 x wheel     672 Mar 31 12:27  132F56
-rw-r--r-- 1 x wheel 2935642 Mar 31 12:27  132F56.zlib
-rw-r--r-- 1 x wheel  130048 Mar 31 12:27  3DFEB0.zip
-rw-r--r-- 1 x wheel    1012 Mar 31 12:27  8EAF
-rw-r--r-- 1 x wheel 4156417 Mar 31 12:27  8EAF.7z
-rw-r--r-- 1 x wheel    1448 Aug 16  2017 '[Content_Types].xml'
drwxr-xr-x 2 x wheel    4096 Mar 31 12:27  docProps
drwxr-xr-x 2 x wheel    4096 Mar 31 12:27  _rels
drwxr-xr-x 5 x wheel    4096 Mar 31 12:27  word
```

Kami pun memeriksa file - file tersebut satu persatu namun tidak menemukan apapun. <br />
Kali ini kami mencoba menggunakan tool **foremost** untuk mengextract data - datanya. 

```

❯ foremost recovered_disk.img
Processing: recovered_disk.img
|foundat=_rels/.rels��MKA
                         ��C��l+����"Bo"�����3i���A
κP��Ǽy���m�ΠN���AêiAq0Ѻ0jx�=/`�/�W>��J�\*�ބ�aI���L�41q��!fOR�<b"���qݶ�2��1��j�[���H�76z�$�&f^�\��8.Nyd�`�y�q�j4�
                                                                                                                       ��S4G�A�y�Y8X���(�[Fw�i4o|˼�l�^�͢��#
�*|

```

Menghasilkan directory *output*

```
❯ ls -l output
total 28K
drwxr-xr-- 6 x wheel 4.0K Mar 31 12:32 .
drwxr-xr-x 4 x wheel 4.0K Mar 31 12:32 ..
drwxr-xr-- 2 x wheel 4.0K Mar 31 12:32 jpg
drwxr-xr-- 2 x wheel 4.0K Mar 31 12:32 pdf
drwxr-xr-- 2 x wheel 4.0K Mar 31 12:32 png
drwxr-xr-- 2 x wheel 4.0K Mar 31 12:32 zip
-rw-r--r-- 1 x wheel 1000 Mar 31 12:32 audit.txt
```

Setelah diperiksa.
Flag ternyata ada di directory *png*

### FLAG

```
gigem{wh3r3_w3r3_601n6_w3_d0n7_n33d_h34d3r5}

```
