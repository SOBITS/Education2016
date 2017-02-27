#!/usr/bin/env python
# coding: utf-8

"""
	demo for speech_recognition @ TurtleBot lecture
	coded by hirono on 23/01/2016
"""

import roslib; roslib.load_manifest('rospeex_if')
import rospy
import datetime
from std_msgs.msg import String
from rospeex_if import ROSpeexInterface
import sys, termios
import re

#parameters for ...
OPERATION_TIME = 500
_operation_count = 0
rule = "none"
point = 1
original = 0
rospeex = None 
turtle_pub = None
_operation_count = 0
_pattern_rule = ""

class SpeechDemo:
    def __init__(self):
		print("********START SPEECH DEMO********")
		rospy.sleep(2)
		rospeex.say('準備が完了しました。質問をお願いします。', 'ja', 'nict')
		rospy.sleep(1)
		self.voice = rospy.Publisher('voice', String, queue_size=10)
		self.num = []
		self.rotate = []

#CallBack__Function for voice recognition
def sr_response(msg):
	print 'You Said : \"%s\"' %msg

	if 'ドイツ' in msg or '伯爵' in msg:
		rospeex.say('飛行船を発明したドイツの伯爵は、ツェッペリン伯爵です。', 'ja', 'nict')
		rospy.sleep(2)
	elif 'アメリカ' in msg and '大統領' in msg:
		rospeex.say('アメリカ合衆国の初代大統領は、ジョージワシントンです。', 'ja', 'nict')
		rospy.sleep(2)
	elif '中国' in msg and '献上' in msg:
		rospeex.say('古代中国で皇帝に献上された肉は、豚肉です。', 'ja', 'nict')
		rospy.sleep(1)
	elif '建造' in msg or '都市' in msg:
		rospeex.say('タイタニック号が建造された都市は、ベルファストです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '女王' in msg or '子供' in msg or '何人' in msg:
		rospeex.say('ビクトリア女王には子供が、9人いました。', 'ja', 'nict')
		rospy.sleep(1)
	elif '太陽' in msg or 'フランス' in msg:
		rospeex.say('太陽王と呼ばれたフランスの王は、ルイ14世です。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'イギリス' in msg or 'ローマ帝国' in msg:
		rospeex.say('イギリスにあるローマ帝国の北の国境に築かれた物は、ハドリアンヌの壁です。', 'ja', 'nict')
		rospy.sleep(1)
	elif '千九百七十九' in msg or '映画' in msg or 'ストロボ' in msg:
		rospeex.say('宇宙貨物船ノストロモ号が出てくる千九百七十九年公開の映画は、エイリアンです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '最初' in msg and '国王' in msg:
		rospeex.say('ベルギーの最初の国王は、レオパルド1世です。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'ニューヨーク' in msg:
		rospeex.say('ニューヨークはかつて、ニューアムステルダムと呼ばれていました。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'ローマ時代' in msg:
		rospeex.say('ローマ時代におけるパリのラテン語名は、ルーテティアです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '千九百一' in msg or 'オーストラリア' in msg or '千九百二十七' in msg:
		rospeex.say('千九百一年から千九百二十七年までのオーストラリアの首都は、メルボルンです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '薬' in msg or '化石' in msg or '別名' in msg or '説明' in msg:
		rospeex.say('化石学の別名は、古生物学です。', 'ja', 'nict')
		rospy.sleep(1)
	elif '食べますか' in msg or 'トンボ' in msg or '今後は' in msg or '今度は' in msg:
		rospeex.say('トンボは、蚊を好んで食べます。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'にもかかわらず' in msg or 'センチメートル' in msg or '以上' in msg:
		rospeex.say('飛べないにも関わらず、三十センチメートル以上ジャンプできる昆虫は、ノミです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'ヨーロッパ' in msg or '生息' in msg:
		rospeex.say('ヨーロッパに生息するバイソンは、ヨーロッパバイソンです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '姿' in msg or '魚' in msg:
		rospeex.say('蛇のような姿をしている魚は、うなぎです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '植物' in msg and 'ている' in msg or 'カナダ' in msg:
		rospeex.say('カナダの国旗に描かれている植物は、カエデです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '最大紙' in msg or '虎' in msg or 'はいないし' in msg or '災害' in msg:
		rospeex.say('トラの最大種は、アムールトラです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'マリリンモンロー' in msg or '生まれつき' in msg:
		rospeex.say('マリリンモンローが生まれつき持っていた奇形は、足の指が６本です。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'シンプソン' in msg or '部屋' in msg:
		rospeex.say('シンプソンズの部屋の番号は、７４２号室です。', 'ja', 'nict')
		rospy.sleep(1)
	elif ('中国' in msg and ('貴族' in msg or 'ひざ' in msg)):
		rospeex.say('古代中国で貴族だけが買うことを許された犬は、ペキニーズです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '監督' in msg:
		rospeex.say('レザボア、ドックス、の監督は、クエンティン、タランティーノです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'フォルクスワーゲン' in msg :
		rospeex.say('フォルクスワーゲンビートル、ハービーのカーナンバーは、５３です。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'ジェームズ' in msg or '最高傑作' in msg:
		rospeex.say('ジェームズボンドのパロディ作品のうちで、最高傑作は、オースティン、パワーズです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'スタートレック' in msg or 'エンタープライズ' in msg:
		rospeex.say('スタートレックに出てくる、エンタープライズ号の艦長で、スキンヘッドの人の名前は、キャプテン・ピカードです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '天使に' in msg or '女優' in msg:
		rospeex.say('天使にラブソングを、と、その続編で主演した女優は、ウーピー・ゴールドバーグです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'トップレベル' in msg or 'トップ' in msg:
		rospeex.say('ベルギーを示すトップレベルドメイン名は、ドットビー、イーです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'MP' in msg or '関連する' in msg:
		rospeex.say('MP３の音質に関連する、単位は、Kbpsです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '被災地' in msg or '略語' in msg:
		rospeex.say('計算機の世界において、RAMは、ランダムアクセスメモリーです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '宇宙飛行' in msg and '世界で初めて' in msg:
		rospeex.say('世界で初めて、宇宙飛行をした人は、ユーリ・ガガーリンです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '半球' in msg and '骨' in msg:
		rospeex.say('北半球と南半球では、北半球のほうが恐竜の骨が多く見つかっています。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'コバルト' in msg or 'とは' in msg:
		rospeex.say('コバルトは、青色です。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'カリウム' in msg and '発明' in msg or 'カレー' in msg:
		rospeex.say('加硫ゴムは、グッドイヤーが発明しました。', 'ja', 'nict')
		rospy.sleep(1)
	elif '観測' in msg or '使用' in msg:
		rospeex.say('星を観測するときに、使用するものは、望遠鏡です。', 'ja', 'nict')
		rospy.sleep(1)
	elif '明るさ' in msg or '単位' in msg:
		rospeex.say('明るさを表す単位は、カンデラです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '気圧計' in msg:
		rospeex.say('気圧計を発明したのは、トリチェリです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'アメリカ' in msg and '宇宙飛行士' in msg:
		rospeex.say('アメリカ合衆国で最初の宇宙飛行士は、アラン・シェパードです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '熱気球' in msg or '名字' in msg:
		rospeex.say('熱気球を発明した兄弟の苗字は、モンゴルフィエです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '蒸気機関' in msg and '長期間' in msg:
		rospeex.say('蒸気機関の発明者は、ジェームス・ワットです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '機械' in msg or 'ヘンリー' in msg or 'ビール' in msg:
		rospeex.say('ヘンリー、ミルによって、発明された機械は、タイプライターです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '金属' in msg or '軽い' in msg:
		rospeex.say('最も軽い金属は、アルミニウムです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '原色' in msg and '何色' in msg:
		rospeex.say('色の３原色は、シアン、イエロー、マゼンタです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '万里の長城' in msg and '中国' in msg:
		rospeex.say('中国の万里の長城は、六千二百五十九キロメートルです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '太陽' in msg or 'バス停' in msg or '潰瘍' in msg:
		rospeex.say('太陽に最も近い惑星は、水星です。', 'ja', 'nict')
		rospy.sleep(1)
	elif '誤字脱字' in msg or '数' in msg:
		rospeex.say('五桁の数字の中で、最大の数は、九万九千九百九十九です。', 'ja', 'nict')
		rospy.sleep(1)
	elif '人間' in msg and '骨' in msg or '安い' in msg:
		rospeex.say('人間の骨の中で、最も骨折しやすい骨は、鎖骨です。', 'ja', 'nict')
		rospy.sleep(1)
	elif '月と夜' in msg or '依頼' in msg or '南アメリカ' in msg:
		rospeex.say('ヴェネツィアに由来する国名を持つ南アメリカの国は、ベネズエラです。', 'ja', 'nict')
		rospy.sleep(1)
	elif 'ニュージーランド' in msg or 'ＮＺ' in msg:
		rospeex.say('ニュージーランドの国旗に書かれている星は、４つです。', 'ja', 'nict')
		rospy.sleep(1)
	elif '赤' in msg and '白' in msg or 'ベルト' in msg:
		rospeex.say('赤と白を混ぜると、ピンクになります。', 'ja', 'nict')
		rospy.sleep(1)

if __name__=="__main__":	
	rospy.init_node('speech_demo')
	#rospeex 
	settings = termios.tcgetattr(sys.stdin)
	rospeex = ROSpeexInterface()
	rospeex.init()
	rospeex.register_sr_response(sr_response)
	rospeex.set_spi_config(language='ja',engine='nict')

try:
	sd = SpeechDemo()
	rospy.spin()
	
except:
        pass

