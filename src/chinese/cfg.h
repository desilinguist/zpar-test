// Copyright (C) University of Oxford 2010
/****************************************************************
 *                                                              *
 * cfg.h - the definitions for chinese cfg                      *
 *                                                              *
 * Author: Yue Zhang                                            *
 *                                                              *
 * Computing Laboratory, Oxford. 2006.10                        *
 *                                                              *
 ****************************************************************/

#ifndef _CHINESE_CFG_H
#define _CHINESE_CFG_H

#include "tags.h"
#include "cfg/penn.h"

//namespace chinese {
//
//inline unsigned long encodeConstituents(const unsigned long &con1, const unsigned long &con2) {
//   return (con1<<CConstituentLabel::SIZE) | con2;
//}
//inline unsigned long int encodeConstituents(const unsigned long &con1, const unsigned long &con2, const unsigned long &con3) {
//   return (con1<<CConstituentLabel::SIZE*2) | (con2<<CConstituentLabel::SIZE) | con3 ;
//}
//inline unsigned long int encodeConstituents(const unsigned long &con1, const unsigned long &con2, const unsigned long &con3, const unsigned long &con4) {
//   return (con1<<CConstituentLabel::SIZE*3) | (con2<<CConstituentLabel::SIZE*2) |
//          (con3<<CConstituentLabel::SIZE) | con4 ;
//}
//
//inline unsigned long int encodeConstituents(const CConstituentLabel &con1, const CConstituentLabel &con2) {
//   return (con1.code()<<CConstituentLabel::SIZE) | con2.code();
//}
//inline unsigned long int encodeConstituents(const CConstituentLabel &con1, const CConstituentLabel &con2, const CConstituentLabel &con3) {
//   return (con1.code()<<CConstituentLabel::SIZE*2) | (con2.code()<<CConstituentLabel::SIZE) | con3.code() ;
//}
//inline unsigned long int encodeConstituents(const CConstituentLabel &con1, const CConstituentLabel &con2, const CConstituentLabel &con3, const CConstituentLabel &con4) {
//   return (con1.code()<<CConstituentLabel::SIZE*3) | (con2.code()<<CConstituentLabel::SIZE*2) |
//          (con3.code()<<CConstituentLabel::SIZE) | con4.code() ;
//}
//
//}; // namespace chinese

//===============================================================

//inline unsigned long hash(const chinese::CConstituentLabel &con) { return con.code();}

//===============================================================

inline istream & operator >> (istream &is, chinese::CConstituentLabel &con) {
   string s;
   is >> s;
   con.load(s);
   return is;
}

inline ostream & operator << (ostream &os, const chinese::CConstituentLabel &con) {
   os << con.str() ;
   return os;
}

#endif
