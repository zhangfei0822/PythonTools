/**
 * Retail MAC
 * 
 * current GPCrypto doesn't support IV Crypto.DES_MAC_EMV 
 */
function getMAC(card,KeyObj,bsApdu)
{       
        bsIV = new ByteString("", HEX);
        bsIV = card.sendApdu(0x00, 0x84, 0x00, 0x00, 0x8, swok);
        bszero = new ByteString("00000000", HEX);
        bsIV = bsIV.left(4).concat( bszero );
        
        msgLen = bsApdu.length;
        paddingLen = 8 - (msgLen % 8)
        if(paddingLen > 0){
        	bsApdu = bsApdu.concat(new ByteString("80", HEX));
        	for(i=0;i<paddingLen-1;i++){
        		bsApdu = bsApdu.concat(new ByteString("00", HEX));
        	}
        }
        	    
        len = bsApdu.length;
        
        left_key_value = KeyObj.getComponent(Key.DES).left(8);
        left_key = new Key();
        left_key.setComponent(Key.DES,left_key_value);
        bsMAC = this.crypto.encrypt(left_key,Crypto.DES_CBC, bsApdu.bytes(0,len-8), bsIV).right(8);
        
        bsMAC = bsMAC.xor( bsApdu.bytes(len-8));
           
        bsMAC = this.crypto.encrypt(KeyObj,Crypto.DES_ECB, bsMAC);
         
        bsMAC = bsMAC.left(4);
        return bsMAC;
}

function emv_calMac(crypto, key, data, iv) {
	var len = data.length;
	if (key.getComponent(Key.DES).length == 16) {
		left_key_value = key.getComponent(Key.DES).left(8);
		left_key = new Key();
		left_key.setComponent(Key.DES, left_key_value);
		if(len>8){
			bsMAC = crypto.encrypt(left_key, Crypto.DES_CBC,
					data.bytes(0, len - 8), iv).right(8);
			bsMAC = bsMAC.xor(data.bytes(len - 8));
			bsMAC = crypto.encrypt(key, Crypto.DES_ECB, bsMAC);
			bsMAC = bsMAC.left(4);
		}else{
			bsMAC = iv.xor(data.bytes(0,8));
			bsMAC = crypto.encrypt(key, Crypto.DES_ECB, bsMAC);
			bsMAC = bsMAC.left(4);
		}
	} else if (key.getComponent(Key.DES).length == 8) {
		bsMAC = crypto.encrypt(key, Crypto.DES_CBC, data, iv).right(8);
		bsMAC = bsMAC.left(4);
	}
	return bsMAC;
}
function select(card,dfname, first) {
	var fci = card.sendApdu(0x00, 0xA4, 0x04, (first ? 0x00 : 0x02), dfname, 0x00);
	return(fci);
}

	var swok = [0x9000];
	var swok2= [0x9000,0x6A88,0x6A80]
	//
	var card = new Card(_scsh3.reader);
	card.reset(Card.RESET_COLD);
	//
	var crypto = new Crypto();
	//
	var bsPSE = new ByteString("315041592E5359532E4444463031", HEX);
	select(card,bsPSE,true);
	var bsAppAID = new ByteString("A0000003330101", HEX);
	select(card,bsAppAID,true);
	var bsManageKey = new ByteString("0123456789ABCDEF0123456789ABCDEF",HEX);
	var init_key = new Key();
	var bsInitKeyArr = new Array();
	bsInitKeyArr["15"] = new ByteString("23A1193BE64CABD9ECE51F1C2A19460D", HEX);
	bsInitKeyArr["16"] = new ByteString("9D9838833BCE9864AD98E6ADD062A761", HEX);
	bsInitKeyArr["17"] = new ByteString("31E631A894C1261F1662546B045B3DAD", HEX);
	bsInitKeyArr["18"] = new ByteString("DA29D5402A403EA273B6F7D302DCD585", HEX);
	bsInitKeyArr["19"] = new ByteString("C8B34CB654F804D60DD50443A78AF12F", HEX);
	bsInitKeyArr["1A"] = new ByteString("D3455E3716AB68C186E5855E380B4CB3", HEX);
	bsInitKeyArr["1B"] = new ByteString("CD3B4052FBC2D3F797D5491A9D0E20F4", HEX);
	bsInitKeyArr["1C"] = new ByteString("F7DFB03194BCD66E6852709D1FBC0BA1", HEX);
	bsInitKeyArr["1D"] = new ByteString("D0ADC179027CF14F9D6294DCF83E8A67", HEX);
	bsInitKeyArr["1E"] = new ByteString("BA1AFE80FE5E135DE025D64551DFE6AB", HEX);
	//sfi_list = ("13 14 15 16 17 18 19 1A 1B 1C 1D").split(" ");
	sfi_list = ("15 16 17 18 19 1A 1B 1C 1D").split(" ");
	var atc = card.sendApdu(0x80, 0xCA, 0x9F, 0X36,0x00, swok);
	var iv = new ByteString("000000000000",HEX);
	iv = iv.concat(atc.bytes(3,2));  
	var P2;
	for(var index=0;index<sfi_list.length;index++){
		init_key.setComponent(Key.DES,bsInitKeyArr[sfi_list[index]]);
		var encrypt_mange_by_kskek = crypto.encrypt(init_key,Crypto.DES_ECB,bsManageKey);
		print(encrypt_mange_by_kskek.toString(HEX));
		var record_data = new ByteString("00211301020000112233445566778899AABBCCDDEEFF",HEX);
		record_data = encrypt_mange_by_kskek.concat(record_data);
		var append_record_apdu = new ByteString("04E200",HEX);
		P2 = (parseInt(sfi_list[index],16)*8).toString(16);
		append_record_apdu = append_record_apdu.concat(new ByteString(P2,HEX));
		var bs_lens = new ByteString( (record_data.length+4).toString(16),HEX );
		append_record_apdu = append_record_apdu.concat(bs_lens).concat(record_data);
		var logcmd = append_record_apdu;
		append_record_apdu = append_record_apdu.pad(Crypto.ISO9797_METHOD_2);
		var mac = emv_calMac(this.crypto, init_key, append_record_apdu, iv);
		logcmd=logcmd.concat(mac);
		print(sfi_list[index] + ":"+ logcmd.toString(HEX));
		card.sendApdu(0x04, 0xE2, 0x00, parseInt(sfi_list[index],16)*8, record_data.concat(mac), swok);
	}
	init_key.setComponent(Key.DES,bsInitKeyArr["1E"]);
	var encrypt_mange_by_kskek = crypto.encrypt(init_key,Crypto.DES_ECB,bsManageKey);
	record_data = new ByteString("00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",HEX);
	record_data = encrypt_mange_by_kskek.concat(record_data);
	append_record_apdu = new ByteString("04E200",HEX);
	P2 = (parseInt("1E",16)*8).toString(16);
	append_record_apdu = append_record_apdu.concat(new ByteString(P2,HEX));
	bs_lens = new ByteString( (record_data.length+4).toString(16),HEX );
	append_record_apdu = append_record_apdu.concat(bs_lens).concat(record_data);
	var logcmd = append_record_apdu;
	append_record_apdu = append_record_apdu.pad(Crypto.ISO9797_METHOD_2);
	mac = emv_calMac(this.crypto, init_key, append_record_apdu, iv);
	logcmd=logcmd.concat(mac);
	print("1E:"+logcmd.toString(HEX));
	card.sendApdu(0x04, 0xE2, 0x00, parseInt("1E",16)*8, record_data.concat(mac), swok);
	print("Finished")
	
	
	