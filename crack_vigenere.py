#!/usr/bin/env python3

from itertools import cycle
from operator import itemgetter
from collections import Counter
from itertools import zip_longest
import string

class CrackVigenere(object):
    """Automatic and manual decoder/solver for Vigenere's cipher """
    def __init__(self,text,language='English'):
        if language == 'English':
            self.alphabet = string.ascii_uppercase
            self.language_most_common_letters = "ETAOI"
        elif language == 'Spanish':
            self.alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
            self.language_most_common_letters = "EAOSR"
        else:
            raise ValueError('Language must be English or Spanish')

        self.original_text = text
        self.text = self._clean_text(text)

    def _clean_text(self,text):
        """Get the characters that belong to the alphabet"""
        clean_text = ""
        for letter in text.upper():
            if letter in self.alphabet:
                clean_text = ''.join((clean_text,letter))

        return clean_text

    def _rebuilt_text(self,text,original_text):
        """Add the characters extracted before with _clean_text() """
        rebuilt_text = list(text)
        for pos,letter in enumerate(original_text.upper()):
            if letter not in self.alphabet:
                rebuilt_text.insert(pos,letter)

        return ''.join(rebuilt_text)

    def decrypt_text(self,period,manual=False):
        """Decrypt a text encrypted with Vigenere's without knowing the key. """
        subsequences = [[] for i in range(period)]
        for pos,letter in enumerate(self.text):
            subsequences[pos%period].append(letter)
        subsequences = [''.join(subseq) for subseq in subsequences]

        keyword = ""
        subsequences_decrypted = ['' for _ in subsequences]
        for index_subseq, subseq in enumerate(subsequences):
            # mcl(s) = most common letter(s)
            mcls_ciphertext = Counter(subseq).most_common(5)
            mcls_ciphertext.sort(key=itemgetter(1,0),reverse=True)

            mcl_plaintext = self.language_most_common_letters[0]
            encryptions_of_mcl_plaintext = []
            for index_letter,letter in enumerate(mcls_ciphertext):
                encrypted_mcl_plaintext = mcls_ciphertext[index_letter][0]
                offset = (self.alphabet.index(encrypted_mcl_plaintext)
                                - self.alphabet.index(mcl_plaintext))%len(self.alphabet)
                matches = 0
                for letter in mcls_ciphertext:
                    pos = self.alphabet.index(letter[0])
                    decrypted_letter = self.alphabet[(pos-offset)%len(self.alphabet)]
                    if decrypted_letter in self.language_most_common_letters:
                        matches += 1
                encryptions_of_mcl_plaintext.append(
                                                                            (encrypted_mcl_plaintext,matches))

            encryptions_of_mcl_plaintext.sort(key=itemgetter(1),reverse=True)
            total_matches = sum([matches for _,matches
                                                    in encryptions_of_mcl_plaintext])
            encryptions_of_mcl_plaintext = [(letter,
                                                                    "{0:.2f}%".format(100*m/total_matches))
                                                                    for letter,m
                                                                    in encryptions_of_mcl_plaintext]

            if manual:
                print("Possible encryptions of {0} with their probability: {1}".format(
                            mcl_plaintext,encryptions_of_mcl_plaintext))
                while True:
                    encrypted_mcl_plaintext = input(
                                                    "Encryption of {0}: ".format(mcl_plaintext)).upper()
                    if encrypted_mcl_plaintext in self.alphabet:
                        break
                    else:
                        print("Bad character found. Type a letter.")
            else:
                encrypted_mcl_plaintext = encryptions_of_mcl_plaintext[0][0]

            offset = (self.alphabet.index(encrypted_mcl_plaintext)
                                - self.alphabet.index(mcl_plaintext))%len(self.alphabet)
            keyletter = self.alphabet[offset-1]
            keyword += keyletter
            if manual:
                 print("Key: {0}{1}\n".format(keyword,'?'*(period-len(keyword))))

            subseq_deciphered = subseq
            for pos, letter in enumerate(self.alphabet):
                subseq_deciphered = subseq_deciphered.replace(
                        letter,self.alphabet[(pos-offset)%len(self.alphabet)].lower())

            subsequences_decrypted[index_subseq] = subseq_deciphered
            # end for

        subsequences_decrypted_mixed = zip_longest(
                                                                        *subsequences_decrypted,fillvalue='')
        subsequences_decrypted_mixed = [''.join(subseq_mix) for subseq_mix
                                                                        in subsequences_decrypted_mixed]
        plaintext = ''.join(subsequences_decrypted_mixed)
        plaintext = self._rebuilt_text(plaintext,self.original_text)

        return keyword, plaintext

if __name__ == '__main__':
    # Examples in english
    text_period_3 = "A'kd ktdf igacfk nnm edgekw lnmacf'i awahwkd. Sissrj kwhhh nf uhjt nxu szt rzdtdsdj de Gghgc. H opsuwdv R-awplk vkaiswg hf igw szjz mwpq lwd Lpmfwzmhdj Vzlt. Zda szdrw bnetmlh vaak tt kghs ac sabd, dxjw idsgr...ac...qsxm. Lxlw in vxd."
    text_period_6 = "UVGPF HBTNW OGUIQ QYZKJ OBTVM TCVBZ MOQQQ DSJXW BFUIB QXLAM SIXLT ZAZJS FZMBI WYJHA YJMOC WSXAM ZZJWP JGQSL TZBQX LAMSW KGGMH IYAAI ZQAWE XIZJQ QVLAF YAVAZ JSFVG MWAOV HQSOT JMMXQ YWITN UECUL TOIZM BFFPO ILFQE DAVJV FCYMR SZXCX FLUJH XWGOG UUFLU JHBMA EHIUJ FFJOA IWOMY MHSYZ UAFYD ZUBGW MXIVQ ASCNW KZAKY BTEUG FQTFE JZVJY DJMTF NQNQP TZMYV MJFEZ UZJVU INPJX XVGMX GRRCB MWDDH ONFVP MBNUQ DNKFE QVMIO GKJOA ISKWL MFCFJ YVILT ZFWSY ZDAPY GRXUX YAHDN GGMFJ HMMMZ YLMIQ QVLAQ SFZLB MWZZA ZTKFD FTNKZ JNNWW QJHMM MZYLM IQQVL AQSFZ LBMWX DZMTX FCYVJ YDJCA XLUGF AFVXT WZNHB GYLGQ FCYUF FMXFM XGRNY OWWSV NQTFM IXBMW OCUQS KAAXQ XUDDG QSSFD IVTFQ COVIJ QYSMF JEGUB JJFCY VJYDJ FQAWE JHIQG ZZFGN KXVHL TXBJP MWLKD HBMWY DXAYG RVPIX LAXYI SGRHU BJJUV FXWGE KYZNL KJHMM MZYLM IQQVL AQSFZ LBMWZ ZAZTA ENNQQ DXVHO ZAECY LNFFC YKTJZ ZLATX MHYZN UMIMW HAQOS ISVRD HLXZU HMMQX UIYFN DQDHP NKARH TFFPN IEJZM QYKTE QCYZJ LAYUG YGPMU UFLUU YISKT VGMKM XXIVI AFDIV NFMNY VXWIZ PMHGY ZNWTM DIUBN GZNWI UAFVF BTUMN BIHZQ XEEMW ZOBMF JOCCB JUFNI NTMDM YXZTX DWEWG FZNPJ EMBHQ KAOZH BBGDY MWKLT ZWWSK FDNCY AAIUV ILTZX MHDMM UBNGZ JZQSV QKYVI WZXYB MWKRY ZJKUB HQSYM KLWRA ENIZD FAOYB TOTDW PJNQM SIRWD DWISO MNNWK SXGBM NJFCC ASGFZ QIXSB MIUNK QOBIY SXGGM SQQNV TFUWH YVFKI ZFTFK ICCBJ EQIQW ZDPWY OZSDV HBJWP OBMZF MGCMS SNGYZ NYTOM WKDUA YTNTQ MNGFF POBMU MDNOQ YGRCU XUAZZ MANLU NIJAA APMBT VMTNP FLMHY ZNUMC UAIWR VOTYW PJHBM AEKLW RAENI ZDFAO YQSKA AUZFK TZLKN LUUYV XGRXI TTJMM YKTFO ZLVJV UIMBJ SPJZP TFAMC VLLTD MAFUD ZXWGD UBUBN GZVGM WAOVB IXYUQ YVYZQ IYOWG BZIXQ WMWUL HZQXE IHZQX EEMAO CBIXU AHYJF UWHUZ PWPDH AZXRD WQJFF AOVIK NPNEJ JQAOA JLAWY TNWHZ NPFLF CYJFF WJZRZ KFDWM NKNVH SWMBO QMWWR PMMYG NZFQJ NQOBI YLTZL MFJQD HAZXR DWQJF FAOVI KUINP JYDZU BASGG NATXA KJWWL GICBD GROBQ XFMOC WSKAR YPFNQ XIUJL AXUAM LTDMK MWOFU KMWOF NPFLI DFTLA HZOAZ HAIXM RSZYN PJJUX BMXGR ALMJV AHUVI LTZMM HMDDN GTXVP MBNUQ RYPFN QVFAT UAHYB TLTDM PFDXJ QMIKB JNBTJ QHCVI SYZLQ HSAAN PJXUZ LKJMD BYVHQ AAHWB LTDMQ XFAOC UJLAZ HOFYQ DHBMW XPRCW QAAWW TDUIA WKXAM NWYSW ZNPJL DVHYZ AXDTQ SYPMO OTXSM ULZSX DMUSG IDMBM WFDGM YGYVE MWWMG NPJHD JGQXW EJZLJ EAXLI HQZJQ QXLTZ NQRWF JLQXW RMIUY ZQYUZ PSZYX MXGXV NMASX GYGTX EZAZJ YMOCW SLAOB MXMZG CBUSF CINWS ODUTO MEOCK JFARC AYZQO CUJLA GCNYG GMHIY AAIZZ TEFCY YZAOF MISVE JZZFU UVFQS BGNNQ HWFJN PJKAG CLWGO FINGJ AOBMW ZAJXV TOUNN PJLUH YBTEM FYRZK FDWMF JQVFQ YQRJL IQDAA AWIKO CCTIJ QICBB GGGXJ JXMOU TKGDO BMSSF DIVYG AQYZQ GAFNP JMDBY VHQAA NPJEA HYVYL TDMAB WXOYZ NFSNO URWDJ ZBMWZ ZAZTK XZAQY AYVNM IAEXI VYWZO QQQDZ JNXFK EPHBN DFCYZ JAEVH QSNUB IZFLU IAIZL GHHWK XDZYL TEMIX MVMMG CBDFU IYBJW ZNCFY QFCLM JAEII BFFQI XJZLM WYONF ZDHOY ZANYE MGTJJ MYZMO NPJFQ BLWSW QYYLY GNGIE TXRNN MFEMI XENDX IIEGW OJHBJ FFRCT QZMQY IWMPZ UEFCQ ICVLA ROBMS SFDIV WWFPL VXLAW OANFQ NMIXM EPUTY ZQMYE NDXWY VJAFC YZWWE OHWWL DVHYZ AXDNG NFMHY ZNUMP HBNDF CYVJY DJCAL JMINM IZUNW QYALZ HAMAB MCOML EOBMB ZUMFE NFPNI NWWHJ FBBAX GWWSL UIOMY GECUS JLTZZ WZFPV NQTFE JZWZJ ZVNQT FGINQ QLTZV ZNYTO XIDGR EOAYA OZYUJ JSZMJ ZLFCY ZJAEN IUJLT DHOYZ MOCUZ KFNUG YGYTJ MTHXZ QPTKF VHLTF FCYEF JYOBZ JKTJF LBZUX BTJSP NCVYG FCYXF DMXYW KBGNN QHWUI NPJHD JWMXK AAAIN FUIAW ZJDDA PYXGG JTFUQ RYUZK FIIBG WSPCT YQAAQ ZTFSA OTIWQ YMTJL GNHWY KQZEB TKMOC AKQAP LBMAD NNNTJ RMYMI GYWSL WAZFC VLXDJ GBMWO PJWKT UONMW FQNMI SVTVN ZJVIZ GCXLR JLMAW DXIVI MOOIC WKFMO OLDQJ HBMWT DAPUD MIYWK VUBHQ YQMIX LNKOD JTNFQ RYUZK FIIBF DXJQW ZJOMY IYAHZ JZTLQ NNBTV QBYVJ JMOYQ SLAKB GXAOV FDNGX ZHKJS SVCVF FPVAI NFIZG CXLDD MMYGF CYUFB QNNQH ZQDAP YKAAG MJLUI AXMQE DWIQX AMWMB AFCMW ZDRJL KJLTZ GIWNQ GICXF QRGQQ AFVHK DOTDW PMSEZ HOZDR ZXBMW ZZAZT UAHGC SAFTG CXLZJ NTJSP PMBTS PDMBW MEOIN FDXRB QYWBZ IXQWR JLUFF KJZWZ JICCB JTDJN PJJEV MMAAP ZHKJV NTNPJ ADKLM XWZXY PJJQO ILFQT VPMHG YZNWW WMGCH JLTVN BMWUM XMXLU ISQXL UZXCU OUOBW ZJPZM BNFKV HLYZQ TBIAW OJGMY GDZUT NRQOB IYLTZ CZKJQ ZXWRA EDHMC LDDWI GDKWI CSVFJ ICWXD ZYLTE IZWIS FAOQI QCMGI VJSZY UABWI VFSBW YPMBR SWZNP JHXZX OJLTV NEJKT VFTRS DXBIM WMYQM HSZII BYMDI VIHCF CYZJS DZNPT KQRBW FJQVM SNFSO BMIWH JNMJK AAWQA AXMCO MLERB MSOUG FGTMN ZMIYA EACMI OQXUV SWHZL JJKMO CAKAQ YUAQG ZBUAY ZQIYO WGUNN PJNUX NQRGR OBMZF EKYIP SNGYP TJDJL ATXBJ FQHWN MOBFD UOSEJ UMIHM AWDWY AFLUN ZQJVM NFWSY MNICW TAYCM XZQVP GBAFC NPJXM OCOZW AANZF NQGWI SFAOA INFXJ XONFS DHBMW YJNMQ KAANP JZUBB EFQEV HLYZQ CIBJD EJZBM WODNQ JKIZW ISFAO VMXSF DMNNW PVMTT FSVMB MWZZA ZTKNV MQHEA WCTNL KDMNW GYVMU FDXZL OMWFO IBTSX VLOJJ AIYEJ UMIHM AWDWY AFLUN ZQJVM NFWSY MNICW UTGCL WWZVL MXLDD JXJVA ANPJA DNYTK ZAJXI SVDJV JJVAA NPJAD YCOSA FTVGX ASIMA YSFDH OKGDR BQYWE JHTDO QXUVS GFWYA FLUNZ QJVMN FWSYM NUVJY DJCVR AENCA XABKC KFFZJ NDTLQ VHLFF QBLWN FZZQG TJWWY TNWHZ MPJZM NHWYZ UIANT JICCK MLAQI BJFAI IEJSD ZHWYK MOCAK AQYUV IOQRC TQFAO VMXSF DMNNW PPHBN DVPMB NUQMI TQKPJ QVQAW ZQIYW DNUVI JUBBB JGGNH MXKXD EMFEU BBBDK FMYIR AMHHW YMZHC VIXGG NPFLE JGMTX KJOPF NQXIU JZQMY WZLAA AZJSF OLQFD EVHLY JUWOT FLUJH AXGYZ INDGG CUDJU AHYNW WECZZ TEZVL ZTOVV CTHWX GMATE QJZGT MTVPM HGYZZ ZTEMM YIXOT ZLMDG GMKCJ KFAIZ KJQZX WRDQA NGTMN VNBJJ QYVGY ZQNNW WEEJZ XJJEZ WCYAA IUVIK FVAOJ JQYVG YZQRC VIKAA JWQAO ZVZZL MGCBD QAPBI AWNZY VYZQQ YBJJM IMWKU DZUBN NQNON KWDDH OHGZO CVZWF JQWWC IDNPY ZQAUQ YZFCU BZFQV LVJVE PZNJJ UIAQX JQYYU ULUQY OTTMX EBTEU NMQXK UKJQL GNVWS YGMGU JFEMB IJFUW OIATM FCWIW GXDHI LGNVW SYGSZ IZLAM BIJFU WOITT MUNCI SSSJV IHCFJ NPJKX PGAFF PBBMY LANIN TMDII ZYZQM HKNLU ZMSSG IDHOY ZMOMW RWTJQ BMAEN CBZSF DIVHS ZVHLB AXGVM HZMIA MIDQO OASGF RUTQG IDHBM WHVFT JQAAX MXHMD LQXSK OIGTM FJXID EKALQ JFPNM WJNQI NPTMS CQMKS OZNPJ VUAZQ HMXOC MXGRO ILFQM IXBTE AMLWB AEOCT QZMQY IIJQV GQYAE VXZJS YYYMU DKMIW YWPDH BMWMH YZNUM IXZJS YDBIA WMYLM FEFCU BTFQY UGYZU NHIYA AIQQQ DDDMM ZHMIX TNNQJ OBYZQ OLCJE QVHQS YAACB XUDZY LBWTJ FLYZQ NYBWM FCMBT TQNYT KWHDX MSLFC UBFDX HYVFJ QXLMF LQYYY ZSXDB IAWMY LMFEF CUBTF QYUGT FFCYZ JVTDF TXGRB YWWYU VNPJK AIMWK XAMGM WKXVP MXSZY NPJKA IMWKX AMGMW KXVPM TOZZL ABAXG VMFTX ZNWXA FYIES LABYB MWDVN BMWFV VTJGR WLWYZ QMBWT VUCUD JSPMY IRLTV NWSWP VSMAW ZOBMX LMOYW KEUNM QXKUK JQFKF VNMXO QGNMW AZBQQ YZFCY PJSFJ ZQSBG NNQHW ERYTY WDDHO BAFCN PJZQV NWKGB KLMXK UJHEN DXWYB WSZNZ WWEQY CVYGM IIIXA EJZNW WQYIU FFPEO AYAOZ CPFNQ VXZJS YOBIY EKAIC WDUON TJUTD FLWWZ RCTQG ZZXID DUQYQ SSZVN QTFIC YZJLT ZSEND XIIBG WVPXO JVNTN PJUAG IZTXF CYQWK WDHJZ LNTNP JUAIN MSLAA NPJAD XBIWS OOYZN ZMQYI IJQVG BTVMT CPFNQ VXZJS YOBIY GZZXI DVARH QSSXV VIRSI DNPNL EQCKN GGNLI HAEOM ENLTD NALGH ZLVTJ TVPQS YTDMT NHEYL QUHUI AENLT OBMBG DYMWK AZOYZ UGEDN QTFMI XVZDX DZQHS FDIVY ZMOIV JVMTL QLZFY IESAZ VFIGS YVFQY LXZVT FUWWI GXSZY VTFUW BCZQK IDFTG WMWFM YGVJC VMSZY MENLT GCBYD QRBQY WNJSA FFPRB QYWSD LTXSE NCAYW DNUVI TDJNP JJEDB IAWMY LMFEF JXIDA TVPMF VDZUU YZMOI VJVMT YDJJK QUTQW KNBIQ DNZYF MSXOY LJNQM SPNDX VHLRG GININ FECUT QTQHU LJDAR NPJJA PAPUD MXYAB AXGVM RSPZJ TFAZV HLYZQ XLWTC QYJTF UQNQQ QDNZG IIWEO LINYT OUVIL TZATT JKJZB MWXJL LXZMG FJJJQ QYIQW PVHLF DXAFM XZECU TQKQZ CBYGS ZNPJJ FCCAN KAPLP THQOB QXAEO BMKSU OBBMS FDQQQ DSJVI HCFJN PJKAP NPBAF CQQYZ FCCAK SUOBE JOUGF JJSNG YBTZQ RICYG ROBMR GGINI NFAAX MXHMD LIXLA IYWKZ AKYEN LTOBQ XXMDN PBWID FTGWM WFMYG FMUVX XAMGB MWVVH OQAZB XQXUA MXATX APLVF LUJHQ SLAVV MFMFD ZCQKK HJPTF KJZJW GFCYZ MGAYQ QYZFC CAKSU OBEJO UGFJJ SNGYB TOAME BTYQO BMWLA KLIDL ABYBM WDOIA YJGBA TJLAB YBMWD OIOTL AEUQQ LABYB MWDOI AYSZY OXKGD ALMJV AHNWL WFCYZ PFARC VLLTV NEJOU GFJJX DZYWS WPVSB MAERC TQTQO BMISK RBMSS XGINL GPNWP NDPMY VBAXG VMFTX ZNWXA ZBQQY ZZZQU JSZDH ORQOJ OVYJK OCATX FCYMX OQZNT FFPJZ TNTQM NGTXF CYMNK UIATF FPRBM WWYTZ IYZQM MLNWP GUVIG ROBMU AXBLQ RKBMC LJXDJ GMAWD TGWZF FVCVX APZFM YXDZY LTEDD HOFFP DZIRW DDWIN KFJVM FYDZU BSSFD IVYZU NGCXL NZWWR WFMOM XGXZN NWWQY IUWAZ BZZTE FCYXW GPDAQ TMECC TQLAK MWKFQ RBIRH ECCZJ DQOZZ JWPJG ZNFSA LWRLT ZGQLZ FTGWZ FFVCV XGRIY EDGDF FMYXD ZYLTE DDHOK JAHNP JZQDA PYWZD HOFDX ZAPJF UZMWK HQIHA DDHVH QFDQO ZZJWP JGZNF SALWR LTZMV TOOVJ XJVDJ WSNWE JZKTD AMULT DQOZZ JWPJG ZNFSA LWRLT ZWCWN MXYWZ KEGIX JKAAW IQARJ LVNSN PNVTL AIFGY ZMOFM YXDZY LTEDD HOKJA HNPJK FJHMR GGINI NFAAA MTJSD UTJLR MYMIG YMCVL XDJGT TGWJO BRGGI NINFA ANMSF QNMMJ DQOZZ JWPJG ZNFSA LWRWH ZLGMA XGUVI EAGYP NDXJZ UNKED MANHB DZZTE QQYZD EAPHB FAZNC LJDQO ZZJWP JGZNF SVHLB ZQINP NKTVJ XJFEV HLBZQ IQMFD XJQNW WQYIU WAZBQ PJFIZ FMYAF MCVLX DJGMA WDTPQ QDMBY ISVQQ YZDZM HFMYX DJGMA WDTMB FLQVH LJNQM SKNLK RYEND XWYIG DQOIA UWQYO XYZMO XIDOT ZHIQD AAAWI KOCCT IJQIV TFUWH YVFFP RBQYW YZHRJ OEVHL LWZOC TJKBM IBJKF VHBXS ZYWIY ZAGCK XOUGF JJSNG YBTBA DHPFF PNUVI KUIAQ SLTZQ WWVEJ ZBMWA GXVJY DJMXN JUOOI QXDZY IYDMN NNWWQ VNTFK FOBIS CSJXI QEUBB BDOQV LMKJQ ZUBQS EO"
    print(CrackVigenere(text_period_3,'English').decrypt_text(3,manual=False)) # ROY
    print(CrackVigenere(text_period_6,'English').decrypt_text(6)[0]) # ROY

    # Examples spanish
    text_periodo_4 = "odiow no sah uva nw sah, c weeidlv itpn iñcjrp ijqewvhp,zqwqlvmfjms z cxffñveñzx;c foci bmtevox, uva aidekiqñnwuwms, fj no wenqul nwdñqff,u nq davmawb of yxqwenvuate nqnvua, ¡mitzqgiw ñyfñci!¿rqn lbu zyjav mñpnqua aijjjv,wenqel zyf dj hf znwqaaxbñnq fh byfkx hf hj pvaaxf?odiow no sels fj by sezyfvj,uva uet ydmewmst hn sgñngf;odiow no qlkvf ndi qwmidaby nebisej c tq yscñndb;odiow no rqn e namvbñ npqendb,odiow no rqn egwve z maiuavhf,odiow no rqn ehñjzjw h sgavhf,u nq fh uyñzx, iñ yxqdhdwjlv,xpzxw tqnrbj ts rqn wpj,jyñndi ñevkvjx op avxjavhf.ux wvaws rqn itpxc bndmeabxbo yvjoqsñab gbñoeel,h wpkn uva nq ppas foceeluet hqwpjrisl ui we.¿zyf ab ob rqhb? qv jsavite.¿zyf ab ob rqhb? qve jhdwjlv,yñw bsnxae, vjj jjylmpj,h im ijcpñ kmfj nw qazyfkx:uva csew te weme fo byfkx,c mlb wvawst, odiolb wpj."
    text_periodo_5 = "¿kpj si ev awst? pr thxijhx.¿kpj si ev awst? pro xepxweg,pro iihggp, ñif txvxndc,r zp aprkw pxxi jh fxmzsdi:mzs jiyf zp odio tm ñzsdi,t pdi mpjcem, ñzsdiñ xdc."
    text_periodo_3 = "NO LVHLLI GN GRQQFQHHVGLJ IV DQ ONXRMS GNWDAVRTODMS SXV ZQOÑQEO ÑVLNQGUEP, NQ 1920, SJVD JXDLEU LMIAEGXW GN WXBXLCYFQSP YSÑQEÑÑEENXLLE FXQ FTEYNW SNVLXHLLEV. TE LMID BI IDQGJPHVXD NQ DVEÑQDDA OD EEUQEFQSP MI ÑJW IAIFDIPLMDB VHTEWQZDB HH LEGJ OHCVD, AIVYIFCS D DQD MMVCVLKYFQSP DQLÑSUUI. HV YP CIACS FQJUJHR, VS VN GXNQWJ GRV MPÑSUUEFQSP BYIQGLNQWN TDAE KJOÑJV WJO YJVLJGLXQ. VQQ HUFDAKR, BI SDIGN SECIPNV SXV ONHLX HHT MF. JO KJGHAOR, BIUJ TRBMETI DYVRGMOJV HT THAMRMS GN OD LODEI. HVGRVXUJHR NO SNVLXHR H GRVSFQIPMS HT EÑOSUQXOX HH LMIAEGX C HT OHVKXJNH (QQJTIV, NWSJRRT, VXBS, HCG.), VN TXNHH DWDA IÑ UIWXHR SEVQWNQ TDAE HVGRVXUJV ÑJ GÑJZH."
    print(CrackVigenere(text_periodo_4,'Spanish').decrypt_text(4)) # VIDA
    print(CrackVigenere(text_periodo_5,'Spanish').decrypt_text(5,manual=False))  # SUEÑO
    print(CrackVigenere(text_periodo_3,'Spanish').decrypt_text(3))  # IDC
