#!/usr/bin/env python3

from operator import itemgetter
from collections import Counter
import string

class PolialphabeticCipher(object):
    """Guess the period of a polialphabetic cipher"""
    english_ic = 0.066895
    spanish_ic = 0.076613

    def __init__(self,text,language='English'):
        if language == 'English':
            self.language = 'English'
            self.alphabet = string.ascii_uppercase
            self.language_ic = PolialphabeticCipher.english_ic
        elif language == 'Spanish':
            self.language = 'Spanish'
            self.alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
            self.language_ic = PolialphabeticCipher.spanish_ic
        else:
            raise ValueError('Language must be English or Spanish')

        self.text = self._clean_text(text)

    def _clean_text(self,text):
        """Get the characters that belong to the alphabet"""
        clean_text = ""
        for letter in text.upper():
            if letter in self.alphabet:
                clean_text = ''.join((clean_text,letter))

        return clean_text

    def _get_3_grams(self):
        """Get the 3-grams that are repeated with their occurrences"""
        three_grams = {}
        for i in range(len(self.text)-3+1):
            currentgram = self.text[i:i+3]
            three_grams[currentgram] = three_grams.get(currentgram,0) + 1

        three_grams = sorted(three_grams.items(), key=itemgetter(1), reverse=True)
        three_grams = [(gram,occurrences)
                                    for gram,occurrences in three_grams
                                    if occurrences > 1]

        return three_grams

    def kasiski_method(self):
        """Compute the possible periods using Kasiski's method."""
        ngrams = self._get_3_grams()
        if not ngrams:
            print("Kasiski's method failed: no 3-grams found. Aborting...")
            return

        periods = []
        for ngram,occurrences in ngrams:
            next_pos = 0
            for i in range(occurrences-1):
                current_pos = self.text.find(ngram,next_pos)
                next_pos = self.text.find(ngram,current_pos+1)
                distance = next_pos - current_pos

                for period in range(2,distance+1):
                    if distance % period == 0:
                        periods.append(period)

        periods = Counter(periods).most_common(5)
        total_occurrences = sum([occurrences for _,occurrences in periods])
        periods = [(period,occurrences/total_occurrences)
                            for period,occurrences in periods]

        return periods

    def _ic(self,text):
        """Calculate the index of coincidence"""
        ic = 0
        n = len(text)
        for f in Counter(text).values():
            ic +=  (f*(f-1))/(n*(n-1))

        return float("{0:.6f}".format(ic))

    def _avg_ic(self,period):
        """Calculate the average of the ic of the period-subsequences"""
        subsequences = [[] for i in range(period)]
        for pos,letter in enumerate(self.text):
            subsequences[pos%period].append(letter)
        subsequences = [''.join(subseq) for subseq in subsequences]
        avg_ic = sum([self._ic(subseq) for subseq in subsequences])/period

        return float("{0:.6f}".format(avg_ic))

    def _exp_ic(self,period):
        """Calculate the expected value of the IC for a cipher of period d"""
        d = period
        n = len(self.text)
        return 1/d*(n-d)/(n-1)*self.language_ic + (d-1)/d*n/(n-1)*1/len(self.alphabet)

    def ic_method(self,periods=None):
        """Compute the possible periods using the index of coincidence"""
        if periods is None:
            periods = range(1,21)

        avg_ics = []
        for period in periods:
            avg_ics.append( (period,self._avg_ic(period)) )
        difference_respect_language_ic = [(period,abs(avg_ic-self.language_ic))
                                                                    for period,avg_ic in avg_ics]
        total_diff = sum([1/diff for period,diff
                                    in difference_respect_language_ic])
        p1 = [(period,1/diff/total_diff )
                for period,diff in difference_respect_language_ic]

        text_ic = self._ic(self.text)
        periods_ic = [(period,self._exp_ic(period)) for period in periods]
        difference_respect_text_ic = [(period,abs(period_ic-text_ic))
                                                        for period,period_ic in periods_ic]
        total_diff = sum([1/diff for period,diff
                                    in difference_respect_text_ic])
        p2 = [(period,1/diff/total_diff )
                for period,diff in difference_respect_text_ic]

        periods_with_probability = [(period,p1[index][1]+p2[index][1])
                                                        for index,period in enumerate(periods)]
        periods_with_probability.sort(key=itemgetter(1),reverse=True)
        total_prob = sum([probability for _,probability
                                        in periods_with_probability])
        periods_with_probability = [(period,probability/total_prob)
                                                        for period,probability in periods_with_probability]

        return periods_with_probability

    def guess_period(self):
        """Guess the period of the polialphabetic cipher using Kasiski's and IC method"""
        kasiski = self.kasiski_method()
        kasiski.sort()
        if not kasiski:
            return
        periods = [period for period,_ in kasiski]
        ic = self.ic_method(periods)
        ic.sort()

        if self.language == 'Spanish':
            weight = 0.1
        else:
            weight = 1
        guessed_periods = [(period,kasiski[index][1]+weight*ic[index][1])
                                            for index,period in enumerate(periods)]

        guessed_periods.sort(key=itemgetter(1),reverse=True)
        total_prob = sum([probability
                                        for _,probability in guessed_periods])
        guessed_periods = [(period,"{0:.2f}%".format(100*probability/total_prob))
                                            for period,probability in guessed_periods]

        return guessed_periods

if __name__ == '__main__':
    # Examples english
    text_period_3 = "A'kd ktdf igacfk nnm edgekw lnmacf'i awahwkd. Sissrj kwhhh nf uhjt nxu szt rzdtdsdj de Gghgc. H opsuwdv R-awplk vkaiswg hf igw szjz mwpq lwd Lpmfwzmhdj Vzlt. Zda szdrw bnetmlh vaak tt kghs ac sabd, dxjw idsgr...ac...qsxm. Lxlw in vxd."
    text_period_6 = "UVGPF HBTNW OGUIQ QYZKJ OBTVM TCVBZ MOQQQ DSJXW BFUIB QXLAM SIXLT ZAZJS FZMBI WYJHA YJMOC WSXAM ZZJWP JGQSL TZBQX LAMSW KGGMH IYAAI ZQAWE XIZJQ QVLAF YAVAZ JSFVG MWAOV HQSOT JMMXQ YWITN UECUL TOIZM BFFPO ILFQE DAVJV FCYMR SZXCX FLUJH XWGOG UUFLU JHBMA EHIUJ FFJOA IWOMY MHSYZ UAFYD ZUBGW MXIVQ ASCNW KZAKY BTEUG FQTFE JZVJY DJMTF NQNQP TZMYV MJFEZ UZJVU INPJX XVGMX GRRCB MWDDH ONFVP MBNUQ DNKFE QVMIO GKJOA ISKWL MFCFJ YVILT ZFWSY ZDAPY GRXUX YAHDN GGMFJ HMMMZ YLMIQ QVLAQ SFZLB MWZZA ZTKFD FTNKZ JNNWW QJHMM MZYLM IQQVL AQSFZ LBMWX DZMTX FCYVJ YDJCA XLUGF AFVXT WZNHB GYLGQ FCYUF FMXFM XGRNY OWWSV NQTFM IXBMW OCUQS KAAXQ XUDDG QSSFD IVTFQ COVIJ QYSMF JEGUB JJFCY VJYDJ FQAWE JHIQG ZZFGN KXVHL TXBJP MWLKD HBMWY DXAYG RVPIX LAXYI SGRHU BJJUV FXWGE KYZNL KJHMM MZYLM IQQVL AQSFZ LBMWZ ZAZTA ENNQQ DXVHO ZAECY LNFFC YKTJZ ZLATX MHYZN UMIMW HAQOS ISVRD HLXZU HMMQX UIYFN DQDHP NKARH TFFPN IEJZM QYKTE QCYZJ LAYUG YGPMU UFLUU YISKT VGMKM XXIVI AFDIV NFMNY VXWIZ PMHGY ZNWTM DIUBN GZNWI UAFVF BTUMN BIHZQ XEEMW ZOBMF JOCCB JUFNI NTMDM YXZTX DWEWG FZNPJ EMBHQ KAOZH BBGDY MWKLT ZWWSK FDNCY AAIUV ILTZX MHDMM UBNGZ JZQSV QKYVI WZXYB MWKRY ZJKUB HQSYM KLWRA ENIZD FAOYB TOTDW PJNQM SIRWD DWISO MNNWK SXGBM NJFCC ASGFZ QIXSB MIUNK QOBIY SXGGM SQQNV TFUWH YVFKI ZFTFK ICCBJ EQIQW ZDPWY OZSDV HBJWP OBMZF MGCMS SNGYZ NYTOM WKDUA YTNTQ MNGFF POBMU MDNOQ YGRCU XUAZZ MANLU NIJAA APMBT VMTNP FLMHY ZNUMC UAIWR VOTYW PJHBM AEKLW RAENI ZDFAO YQSKA AUZFK TZLKN LUUYV XGRXI TTJMM YKTFO ZLVJV UIMBJ SPJZP TFAMC VLLTD MAFUD ZXWGD UBUBN GZVGM WAOVB IXYUQ YVYZQ IYOWG BZIXQ WMWUL HZQXE IHZQX EEMAO CBIXU AHYJF UWHUZ PWPDH AZXRD WQJFF AOVIK NPNEJ JQAOA JLAWY TNWHZ NPFLF CYJFF WJZRZ KFDWM NKNVH SWMBO QMWWR PMMYG NZFQJ NQOBI YLTZL MFJQD HAZXR DWQJF FAOVI KUINP JYDZU BASGG NATXA KJWWL GICBD GROBQ XFMOC WSKAR YPFNQ XIUJL AXUAM LTDMK MWOFU KMWOF NPFLI DFTLA HZOAZ HAIXM RSZYN PJJUX BMXGR ALMJV AHUVI LTZMM HMDDN GTXVP MBNUQ RYPFN QVFAT UAHYB TLTDM PFDXJ QMIKB JNBTJ QHCVI SYZLQ HSAAN PJXUZ LKJMD BYVHQ AAHWB LTDMQ XFAOC UJLAZ HOFYQ DHBMW XPRCW QAAWW TDUIA WKXAM NWYSW ZNPJL DVHYZ AXDTQ SYPMO OTXSM ULZSX DMUSG IDMBM WFDGM YGYVE MWWMG NPJHD JGQXW EJZLJ EAXLI HQZJQ QXLTZ NQRWF JLQXW RMIUY ZQYUZ PSZYX MXGXV NMASX GYGTX EZAZJ YMOCW SLAOB MXMZG CBUSF CINWS ODUTO MEOCK JFARC AYZQO CUJLA GCNYG GMHIY AAIZZ TEFCY YZAOF MISVE JZZFU UVFQS BGNNQ HWFJN PJKAG CLWGO FINGJ AOBMW ZAJXV TOUNN PJLUH YBTEM FYRZK FDWMF JQVFQ YQRJL IQDAA AWIKO CCTIJ QICBB GGGXJ JXMOU TKGDO BMSSF DIVYG AQYZQ GAFNP JMDBY VHQAA NPJEA HYVYL TDMAB WXOYZ NFSNO URWDJ ZBMWZ ZAZTK XZAQY AYVNM IAEXI VYWZO QQQDZ JNXFK EPHBN DFCYZ JAEVH QSNUB IZFLU IAIZL GHHWK XDZYL TEMIX MVMMG CBDFU IYBJW ZNCFY QFCLM JAEII BFFQI XJZLM WYONF ZDHOY ZANYE MGTJJ MYZMO NPJFQ BLWSW QYYLY GNGIE TXRNN MFEMI XENDX IIEGW OJHBJ FFRCT QZMQY IWMPZ UEFCQ ICVLA ROBMS SFDIV WWFPL VXLAW OANFQ NMIXM EPUTY ZQMYE NDXWY VJAFC YZWWE OHWWL DVHYZ AXDNG NFMHY ZNUMP HBNDF CYVJY DJCAL JMINM IZUNW QYALZ HAMAB MCOML EOBMB ZUMFE NFPNI NWWHJ FBBAX GWWSL UIOMY GECUS JLTZZ WZFPV NQTFE JZWZJ ZVNQT FGINQ QLTZV ZNYTO XIDGR EOAYA OZYUJ JSZMJ ZLFCY ZJAEN IUJLT DHOYZ MOCUZ KFNUG YGYTJ MTHXZ QPTKF VHLTF FCYEF JYOBZ JKTJF LBZUX BTJSP NCVYG FCYXF DMXYW KBGNN QHWUI NPJHD JWMXK AAAIN FUIAW ZJDDA PYXGG JTFUQ RYUZK FIIBG WSPCT YQAAQ ZTFSA OTIWQ YMTJL GNHWY KQZEB TKMOC AKQAP LBMAD NNNTJ RMYMI GYWSL WAZFC VLXDJ GBMWO PJWKT UONMW FQNMI SVTVN ZJVIZ GCXLR JLMAW DXIVI MOOIC WKFMO OLDQJ HBMWT DAPUD MIYWK VUBHQ YQMIX LNKOD JTNFQ RYUZK FIIBF DXJQW ZJOMY IYAHZ JZTLQ NNBTV QBYVJ JMOYQ SLAKB GXAOV FDNGX ZHKJS SVCVF FPVAI NFIZG CXLDD MMYGF CYUFB QNNQH ZQDAP YKAAG MJLUI AXMQE DWIQX AMWMB AFCMW ZDRJL KJLTZ GIWNQ GICXF QRGQQ AFVHK DOTDW PMSEZ HOZDR ZXBMW ZZAZT UAHGC SAFTG CXLZJ NTJSP PMBTS PDMBW MEOIN FDXRB QYWBZ IXQWR JLUFF KJZWZ JICCB JTDJN PJJEV MMAAP ZHKJV NTNPJ ADKLM XWZXY PJJQO ILFQT VPMHG YZNWW WMGCH JLTVN BMWUM XMXLU ISQXL UZXCU OUOBW ZJPZM BNFKV HLYZQ TBIAW OJGMY GDZUT NRQOB IYLTZ CZKJQ ZXWRA EDHMC LDDWI GDKWI CSVFJ ICWXD ZYLTE IZWIS FAOQI QCMGI VJSZY UABWI VFSBW YPMBR SWZNP JHXZX OJLTV NEJKT VFTRS DXBIM WMYQM HSZII BYMDI VIHCF CYZJS DZNPT KQRBW FJQVM SNFSO BMIWH JNMJK AAWQA AXMCO MLERB MSOUG FGTMN ZMIYA EACMI OQXUV SWHZL JJKMO CAKAQ YUAQG ZBUAY ZQIYO WGUNN PJNUX NQRGR OBMZF EKYIP SNGYP TJDJL ATXBJ FQHWN MOBFD UOSEJ UMIHM AWDWY AFLUN ZQJVM NFWSY MNICW TAYCM XZQVP GBAFC NPJXM OCOZW AANZF NQGWI SFAOA INFXJ XONFS DHBMW YJNMQ KAANP JZUBB EFQEV HLYZQ CIBJD EJZBM WODNQ JKIZW ISFAO VMXSF DMNNW PVMTT FSVMB MWZZA ZTKNV MQHEA WCTNL KDMNW GYVMU FDXZL OMWFO IBTSX VLOJJ AIYEJ UMIHM AWDWY AFLUN ZQJVM NFWSY MNICW UTGCL WWZVL MXLDD JXJVA ANPJA DNYTK ZAJXI SVDJV JJVAA NPJAD YCOSA FTVGX ASIMA YSFDH OKGDR BQYWE JHTDO QXUVS GFWYA FLUNZ QJVMN FWSYM NUVJY DJCVR AENCA XABKC KFFZJ NDTLQ VHLFF QBLWN FZZQG TJWWY TNWHZ MPJZM NHWYZ UIANT JICCK MLAQI BJFAI IEJSD ZHWYK MOCAK AQYUV IOQRC TQFAO VMXSF DMNNW PPHBN DVPMB NUQMI TQKPJ QVQAW ZQIYW DNUVI JUBBB JGGNH MXKXD EMFEU BBBDK FMYIR AMHHW YMZHC VIXGG NPFLE JGMTX KJOPF NQXIU JZQMY WZLAA AZJSF OLQFD EVHLY JUWOT FLUJH AXGYZ INDGG CUDJU AHYNW WECZZ TEZVL ZTOVV CTHWX GMATE QJZGT MTVPM HGYZZ ZTEMM YIXOT ZLMDG GMKCJ KFAIZ KJQZX WRDQA NGTMN VNBJJ QYVGY ZQNNW WEEJZ XJJEZ WCYAA IUVIK FVAOJ JQYVG YZQRC VIKAA JWQAO ZVZZL MGCBD QAPBI AWNZY VYZQQ YBJJM IMWKU DZUBN NQNON KWDDH OHGZO CVZWF JQWWC IDNPY ZQAUQ YZFCU BZFQV LVJVE PZNJJ UIAQX JQYYU ULUQY OTTMX EBTEU NMQXK UKJQL GNVWS YGMGU JFEMB IJFUW OIATM FCWIW GXDHI LGNVW SYGSZ IZLAM BIJFU WOITT MUNCI SSSJV IHCFJ NPJKX PGAFF PBBMY LANIN TMDII ZYZQM HKNLU ZMSSG IDHOY ZMOMW RWTJQ BMAEN CBZSF DIVHS ZVHLB AXGVM HZMIA MIDQO OASGF RUTQG IDHBM WHVFT JQAAX MXHMD LQXSK OIGTM FJXID EKALQ JFPNM WJNQI NPTMS CQMKS OZNPJ VUAZQ HMXOC MXGRO ILFQM IXBTE AMLWB AEOCT QZMQY IIJQV GQYAE VXZJS YYYMU DKMIW YWPDH BMWMH YZNUM IXZJS YDBIA WMYLM FEFCU BTFQY UGYZU NHIYA AIQQQ DDDMM ZHMIX TNNQJ OBYZQ OLCJE QVHQS YAACB XUDZY LBWTJ FLYZQ NYBWM FCMBT TQNYT KWHDX MSLFC UBFDX HYVFJ QXLMF LQYYY ZSXDB IAWMY LMFEF CUBTF QYUGT FFCYZ JVTDF TXGRB YWWYU VNPJK AIMWK XAMGM WKXVP MXSZY NPJKA IMWKX AMGMW KXVPM TOZZL ABAXG VMFTX ZNWXA FYIES LABYB MWDVN BMWFV VTJGR WLWYZ QMBWT VUCUD JSPMY IRLTV NWSWP VSMAW ZOBMX LMOYW KEUNM QXKUK JQFKF VNMXO QGNMW AZBQQ YZFCY PJSFJ ZQSBG NNQHW ERYTY WDDHO BAFCN PJZQV NWKGB KLMXK UJHEN DXWYB WSZNZ WWEQY CVYGM IIIXA EJZNW WQYIU FFPEO AYAOZ CPFNQ VXZJS YOBIY EKAIC WDUON TJUTD FLWWZ RCTQG ZZXID DUQYQ SSZVN QTFIC YZJLT ZSEND XIIBG WVPXO JVNTN PJUAG IZTXF CYQWK WDHJZ LNTNP JUAIN MSLAA NPJAD XBIWS OOYZN ZMQYI IJQVG BTVMT CPFNQ VXZJS YOBIY GZZXI DVARH QSSXV VIRSI DNPNL EQCKN GGNLI HAEOM ENLTD NALGH ZLVTJ TVPQS YTDMT NHEYL QUHUI AENLT OBMBG DYMWK AZOYZ UGEDN QTFMI XVZDX DZQHS FDIVY ZMOIV JVMTL QLZFY IESAZ VFIGS YVFQY LXZVT FUWWI GXSZY VTFUW BCZQK IDFTG WMWFM YGVJC VMSZY MENLT GCBYD QRBQY WNJSA FFPRB QYWSD LTXSE NCAYW DNUVI TDJNP JJEDB IAWMY LMFEF JXIDA TVPMF VDZUU YZMOI VJVMT YDJJK QUTQW KNBIQ DNZYF MSXOY LJNQM SPNDX VHLRG GININ FECUT QTQHU LJDAR NPJJA PAPUD MXYAB AXGVM RSPZJ TFAZV HLYZQ XLWTC QYJTF UQNQQ QDNZG IIWEO LINYT OUVIL TZATT JKJZB MWXJL LXZMG FJJJQ QYIQW PVHLF DXAFM XZECU TQKQZ CBYGS ZNPJJ FCCAN KAPLP THQOB QXAEO BMKSU OBBMS FDQQQ DSJVI HCFJN PJKAP NPBAF CQQYZ FCCAK SUOBE JOUGF JJSNG YBTZQ RICYG ROBMR GGINI NFAAX MXHMD LIXLA IYWKZ AKYEN LTOBQ XXMDN PBWID FTGWM WFMYG FMUVX XAMGB MWVVH OQAZB XQXUA MXATX APLVF LUJHQ SLAVV MFMFD ZCQKK HJPTF KJZJW GFCYZ MGAYQ QYZFC CAKSU OBEJO UGFJJ SNGYB TOAME BTYQO BMWLA KLIDL ABYBM WDOIA YJGBA TJLAB YBMWD OIOTL AEUQQ LABYB MWDOI AYSZY OXKGD ALMJV AHNWL WFCYZ PFARC VLLTV NEJOU GFJJX DZYWS WPVSB MAERC TQTQO BMISK RBMSS XGINL GPNWP NDPMY VBAXG VMFTX ZNWXA ZBQQY ZZZQU JSZDH ORQOJ OVYJK OCATX FCYMX OQZNT FFPJZ TNTQM NGTXF CYMNK UIATF FPRBM WWYTZ IYZQM MLNWP GUVIG ROBMU AXBLQ RKBMC LJXDJ GMAWD TGWZF FVCVX APZFM YXDZY LTEDD HOFFP DZIRW DDWIN KFJVM FYDZU BSSFD IVYZU NGCXL NZWWR WFMOM XGXZN NWWQY IUWAZ BZZTE FCYXW GPDAQ TMECC TQLAK MWKFQ RBIRH ECCZJ DQOZZ JWPJG ZNFSA LWRLT ZGQLZ FTGWZ FFVCV XGRIY EDGDF FMYXD ZYLTE DDHOK JAHNP JZQDA PYWZD HOFDX ZAPJF UZMWK HQIHA DDHVH QFDQO ZZJWP JGZNF SALWR LTZMV TOOVJ XJVDJ WSNWE JZKTD AMULT DQOZZ JWPJG ZNFSA LWRLT ZWCWN MXYWZ KEGIX JKAAW IQARJ LVNSN PNVTL AIFGY ZMOFM YXDZY LTEDD HOKJA HNPJK FJHMR GGINI NFAAA MTJSD UTJLR MYMIG YMCVL XDJGT TGWJO BRGGI NINFA ANMSF QNMMJ DQOZZ JWPJG ZNFSA LWRWH ZLGMA XGUVI EAGYP NDXJZ UNKED MANHB DZZTE QQYZD EAPHB FAZNC LJDQO ZZJWP JGZNF SVHLB ZQINP NKTVJ XJFEV HLBZQ IQMFD XJQNW WQYIU WAZBQ PJFIZ FMYAF MCVLX DJGMA WDTPQ QDMBY ISVQQ YZDZM HFMYX DJGMA WDTMB FLQVH LJNQM SKNLK RYEND XWYIG DQOIA UWQYO XYZMO XIDOT ZHIQD AAAWI KOCCT IJQIV TFUWH YVFFP RBQYW YZHRJ OEVHL LWZOC TJKBM IBJKF VHBXS ZYWIY ZAGCK XOUGF JJSNG YBTBA DHPFF PNUVI KUIAQ SLTZQ WWVEJ ZBMWA GXVJY DJMXN JUOOI QXDZY IYDMN NNWWQ VNTFK FOBIS CSJXI QEUBB BDOQV LMKJQ ZUBQS EO"
    print('3?',PolialphabeticCipher(text_period_3,'English').guess_period()) # ROY
    print('6?',PolialphabeticCipher(text_period_6,'English').guess_period()) # LUTHER

    # Examples spanish
    text_periodo_4 = "odiow no sah uva nw sah, c weeidlv itpn iñcjrp ijqewvhp,zqwqlvmfjms z cxffñveñzx;c foci bmtevox, uva aidekiqñnwuwms, fj no wenqul nwdñqff,u nq davmawb of yxqwenvuate nqnvua, ¡mitzqgiw ñyfñci!¿rqn lbu zyjav mñpnqua aijjjv,wenqel zyf dj hf znwqaaxbñnq fh byfkx hf hj pvaaxf?odiow no sels fj by sezyfvj,uva uet ydmewmst hn sgñngf;odiow no qlkvf ndi qwmidaby nebisej c tq yscñndb;odiow no rqn e namvbñ npqendb,odiow no rqn egwve z maiuavhf,odiow no rqn ehñjzjw h sgavhf,u nq fh uyñzx, iñ yxqdhdwjlv,xpzxw tqnrbj ts rqn wpj,jyñndi ñevkvjx op avxjavhf.ux wvaws rqn itpxc bndmeabxbo yvjoqsñab gbñoeel,h wpkn uva nq ppas foceeluet hqwpjrisl ui we.¿zyf ab ob rqhb? qv jsavite.¿zyf ab ob rqhb? qve jhdwjlv,yñw bsnxae, vjj jjylmpj,h im ijcpñ kmfj nw qazyfkx:uva csew te weme fo byfkx,c mlb wvawst, odiolb wpj."
    text_periodo_5 = "¿kpj si ev awst? pr thxijhx.¿kpj si ev awst? pro xepxweg,pro iihggp, ñif txvxndc,r zp aprkw pxxi jh fxmzsdi:mzs jiyf zp odio tm ñzsdi,t pdi mpjcem, ñzsdiñ xdc."
    text_periodo_3 = "NO LVHLLI GN GRQQFQHHVGLJ IV DQ ONXRMS GNWDAVRTODMS SXV ZQOÑQEO ÑVLNQGUEP, NQ 1920, SJVD JXDLEU LMIAEGXW GN WXBXLCYFQSP YSÑQEÑÑEENXLLE FXQ FTEYNW SNVLXHLLEV. TE LMID BI IDQGJPHVXD NQ DVEÑQDDA OD EEUQEFQSP MI ÑJW IAIFDIPLMDB VHTEWQZDB HH LEGJ OHCVD, AIVYIFCS D DQD MMVCVLKYFQSP DQLÑSUUI. HV YP CIACS FQJUJHR, VS VN GXNQWJ GRV MPÑSUUEFQSP BYIQGLNQWN TDAE KJOÑJV WJO YJVLJGLXQ. VQQ HUFDAKR, BI SDIGN SECIPNV SXV ONHLX HHT MF. JO KJGHAOR, BIUJ TRBMETI DYVRGMOJV HT THAMRMS GN OD LODEI. HVGRVXUJHR NO SNVLXHR H GRVSFQIPMS HT EÑOSUQXOX HH LMIAEGX C HT OHVKXJNH (QQJTIV, NWSJRRT, VXBS, HCG.), VN TXNHH DWDA IÑ UIWXHR SEVQWNQ TDAE HVGRVXUJV ÑJ GÑJZH."
    print('4?',PolialphabeticCipher(text_periodo_4,'Spanish').guess_period()) # VIDA
    print('5?',PolialphabeticCipher(text_periodo_5,'Spanish').guess_period()) # SUEÑO
    print('3?',PolialphabeticCipher(text_periodo_3,'Spanish').guess_period()) # IDC

    # Examples english kasiski and IC.
    print('\n3?',PolialphabeticCipher(text_period_3,'English').kasiski_method()) # ROY
    print('6?',PolialphabeticCipher(text_period_6,'English').ic_method()) # LUTHER