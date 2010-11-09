// Copyright (C) University of Oxford 2010
/****************************************************************
 *                                                         
 * test.cpp 
 *                                                          
 * Author: Yue Zhang                                         
 *                                                      
 ****************************************************************/

#define SIMPLE_HASH
#include "definitions.h"
#include "table2.h"
#include "reader.h"
#include "writer.h"
#include "linguistics/conll.h"
#include "linguistics/generictag.h"
#include "linguistics/lemma.h"

class A {
public:
   enum {C=0, D};
};

class B : public A {
public:
   enum {C=A::C+1};
};

void testtable2() {
   CTable2<string, string, double> table2;
   ifstream is("./input.txt");
   is >> table2;
   cout << table2.lookup("'m", "!edge") << endl;
   cout << table2.lookup("OOV", "OOV") << endl;
   cout << table2.lookup("None", "1") << endl;
//   cout << table2;
   is.close();
}

void testreader() {
   CSentenceReader reader("tmp.txt");
   CTwoStringVector sent;
   CSentenceWriter writer;
   while (reader.readTaggedSentence(&sent, false, '/')) {
      writer.writeSentence(&sent);
   }
}

void testconllio() {
   // io
   CCoNLLInput input;
   CCoNLLOutput output;
   while (cin >> input)
      cout << input;
   while (cin >> output) {
      cout << output;
   }
}

void testconlltag() {
   // tag
   CCoNLLCPOS pos;
   pos.load("CPOS a");
   pos.load("CPOS b");
   pos.load("CPOS c");
   for (unsigned i=0; i<pos.getTagset().count(); ++i)
      cout << CCoNLLCPOS(i) << ' ';
   CCoNLLFeats feats;
   feats.load("Feats a");
   feats.load("Feats b");
   feats.load("Feats c");
   for (unsigned i=0; i<feats.getTagset().count(); ++i)
      cout << CCoNLLFeats(i) << ' ';
   cout << endl;
}

void testconllfeats() {
   vector<CCoNLLFeats> feats;
   string s;
   cin >> s;
   readCoNLLFeats(feats, s);
   for (unsigned i=0; i<feats.size(); ++i)
      cout << feats[i] << ' '; 
   cout << endl;
   return;

}

void testgenerictags() {
   class CTag1 : public CGenericTag {
   public:
      CTag1() : CGenericTag() { }
      CTag1(const string &s) : CGenericTag() { load(s); }
      CTag1(const CTag1 &t) : CGenericTag(t) { }
      CTag1(const unsigned long &u) : CGenericTag() { assert(getTagset().count()>u); m_code=u; }
      CGenericTagset &getTagset() const { static CGenericTagset tagset; return tagset; }
   };
   class CTag2 : public CGenericTag {
   public:
      CTag2() : CGenericTag() { }
      CTag2(const string &s) : CGenericTag() { load(s); }
      CTag2(const CTag2 &t) : CGenericTag(t) { }
      CTag2(const unsigned long &u) : CGenericTag() { assert(getTagset().count()>u); m_code=u; }
      CGenericTagset &getTagset() const { static CGenericTagset tagset; return tagset; }
   };
   CTag1 tag1("1a");
   CTag2 tag2("2a");
   CTag1 tag3("1b");
   tag3.load("1c");
   for (unsigned i=0; i<tag1.getTagset().count(); ++i)
      cout << CTag1(i) << ' ';
   cout << endl;
   for (unsigned i=0; i<tag2.getTagset().count(); ++i)
      cout << CTag2(i) << ' ';
   cout << endl;
}

void testlemma() {
   CLemma lemma1("abc");
   CLemma lemma2;
   cin >> lemma2;
   cout << lemma1 << " " << lemma2 << endl;
}

int main(int argc, char**argv){
   try {
//   cout << B::C << B::D << endl;
//   cout << ~0UL << endl;
//   testtable2();
//   testreader();
//   testconllfeats();
//   testgenerictags();
 testlemma();
   }catch(const string &s) { cout << s << endl; }
};

