# オブジェクト指向 分析設計論 

ＯｂｊｅｃｔＯｒｉｅｎｔｅｄＡｎａｌｙｓｉｓ/ ＯｂｊｅｃｔＯｒｉｅｎｔｅｄＤｅｓｉｇｎ 

第１２回 

Ｉ科非常勤講師：西尾公伸 

1 

## ユースケースモデリングの位置づけ 



<!-- Start of picture text -->
要求<br>分析<br>ユースケースに基づく<br>設計<br>設計モデルの構築<br>実装<br>テスト<br>ワークフロー<br><!-- End of picture text -->

## ユースケースモデリングの位置づけ 



<!-- Start of picture text -->
要求<br>分析<br>設計<br>実装<br>テスト<br>ワークフロー<br><!-- End of picture text -->



ソフトウェア部品の流用可能なクラス を洗い出す 

残りのクラスについては、クラス図や シーケンス図に基づき、ひたすらプ ログラミング 

## クラス構造のコード化 



<!-- Start of picture text -->
<クラス名><br><属性名> ：<型名><br>・・・<br><操作名> ( <引数の型> … ) ：<型名><br>・・・<br><!-- End of picture text -->

**`public class`** <クラス名> **`{`** <型名> <インスタンス変数名> ; 

・・・ 

<戻り値の型> <操作名> **`(`** <引数の型> <仮引数名> **`,`** ・・・ `);` 

・・・ 

```
}
```

## クラス構造のコード化 

<クラス名> <属性名> ：<型名> ・・・ <操作名> ( <引数の型> … ) ：<型名> ・・・ 

**`public class`** <クラス名> **`{ static`** <型名> <クラス変数名> ; ・・・ 

**`static`** <戻り値の型> <操作名> **`(`** <引数の型> <仮引数名> **`,`** ・・・ `);` ・・・ 

```
}
```

## クラス構造のコード化 

<クラス名> **`+`** <属性名> ：<型名> **`-`** <属性名> ：<型名> **`#`** <属性名> ：<型名> ・・・ 

**`public class`** <クラス名> **`{ public`** <型名> <インスタンス変数名> **`; private`** <型名> <インスタンス変数名> `;` **`protected`** <型名> <インスタンス変数名> `;` ・・・ 

```
}
```

## クラス構造のコード化 

・・・ 

<クラス名> 

+ <操作名> ( <引数の型> … ) ：<型名> - <操作名> ( <引数の型> … ) ：<型名> # <操作名> ( <引数の型> … ) ：<型名> 

**`public class`** <クラス名> **`{ public`** <型名> <操作名> ( <引数の型> … ) ; **`private`** <型名> <操作名> ( <引数の型> … ) ; **`protected`** <型名> <操作名> ( <引数の型> … ) ; 

・・・ 

```
}
```

## クラス構造のコード化 



<!-- Start of picture text -->
<クラス名><br>・・・ イタリック体<br>・・・<br><!-- End of picture text -->



<!-- Start of picture text -->
abstract class  <クラス名>  {<br>・・・<br>}<br><!-- End of picture text -->

## 関連に関するコーディング 

汎化関連 



<!-- Start of picture text -->
Ｂ<br>Ａ<br>B : A{: A{{ class B extends A{<br>・・・<br>}<br><!-- End of picture text -->



<!-- Start of picture text -->
class B : A{: A{{<br>・・・<br>}<br><!-- End of picture text -->

## 関連に関するコーディング 

### インタフェースと実装クラス 



<!-- Start of picture text -->
<< interface >><br>Ｂ<br>Ａ<br><!-- End of picture text -->



<!-- Start of picture text -->
class B implements A {<br>}<br><!-- End of picture text -->



<!-- Start of picture text -->
interface A {<br>}<br><!-- End of picture text -->

## 関連に関するコーディング 一般的な関連（片方向） 



<!-- Start of picture text -->
Ａ Ｂ<br><!-- End of picture text -->

```
classA {
private B *roleB;
public void setRoleB( B *obj){
roleB=obj;
}
public void resetRoleB( ){
roleB=NULL;
}
```

```
}
```

## 関連に関するコーディング 

#### 一般的な関連（双方向） 

Ａ 

Ｂ 

お互いに同時に接続・ 切断する必要がある 

```
classA {
private B *roleB;
public void setRoleB( B *obj){
releaseRoleB();
roleB=obj;
roleB.setRoleA( this );
}
public void releaseRoleB( ){
if(roleB==NULL) return;
roleB.setRoleA( NULL );
roleB=NULL;
```

```
}
public B getRoleB(){
return roleB;
```

```
}
```

```
}
```

```
classB {
private A *roleA;
public void setRoleA( A *obj){
releaseRoleA();
roleA=obj;
roleA.setRoleB(this);
```

```
}
public void releaseRoleA( ){
if(roleA==NULL) return ;
roleA.setRoleA( NULL );
roleA=NULL;
```

```
}
public A getRoleA(){
return roleA;
}
```

```
}
```

## 動作に関するコーディング 

#### オブジェクトの生成・削除 



<!-- Start of picture text -->
：Ａ<br>public class A {<br>myfunc() private B *objB;<br>：Ｂ<br>public void myfunc(){<br>・・・<br>objB = new B;<br>￥<br>￥<br>・・・<br>delete objB;<br>}<br>}<br><!-- End of picture text -->

## 動作に関するコーディング 

#### オブジェクト間のメッセージ送受信 



<!-- Start of picture text -->
：Ａ ：Ｂ<br>funcA()<br>funcB(v:T)<br>￥<br>￥<br>public class A { public class B {<br>private B *objB;<br>public void funcB(v:T){<br>・・・<br>public void funcA(){<br>・・・ }<br>objB.funcB(v); }<br>・・・<br>}<br>}<br><!-- End of picture text -->

## 動作に関するコーディング 

#### 拡張フラグメント（ａｌｔ） 



<!-- Start of picture text -->
：Ａ ：Ｂ ：Ｃ<br>[value>10000]<br>alt<br>funcB(u:U)<br>￥<br>￥<br>￥ funcC(v:V)<br>funcA()<br>ｚ<br><!-- End of picture text -->



<!-- Start of picture text -->
public class A {<br>public void funcA(){<br>・・・<br>if(value>10000)<br>objB.funcB(u);<br>else<br>objc.funcC(v);<br>}<br>}<br><!-- End of picture text -->

## 動作に関するコーディング 

#### 拡張フラグメント（ｌｏｏｐ） 



<!-- Start of picture text -->
：Ａ ：Ｂ ：Ｃ<br>[ 繰り返し条件 ]<br>loop<br>funcB(u:U)<br>￥<br>￥<br>￥ funcC(v:V)<br>funcA()<br>ｚ<br>public class A {<br>public void funcA(){<br>・・・<br>while( 繰り返し条件 ){<br>objB.funcB(u);<br>objc.funcC(v);<br>}<br>}<br>}<br><!-- End of picture text -->

適用事例 

# 話題沸騰ポット（３ℓタイプ） 



<!-- Start of picture text -->
ポット<br>話題沸騰<br><!-- End of picture text -->

右の記述を満足する ビジネスユースケー スを作成しなさい。 

マイコン制御。 私達の目的はこのマイコンに搭載さ れるソフトウエアを開発すること お湯の温度制御。 （設定された湯温±1℃に維持） 加熱器のオン・オフ センサー（温度計）随時計測可能 ユーザが湯温を設定できる。 （８０度、９０度、９８度の３種類） お湯の量が限界値を下回ったら警告。 ユーザが限界値を設定できる。 １００㏄単位で０ℓ～２ℓ ユーザは蓋（フタ）を開けて水を入れる。 ユーザは「出る」ボタンを押してお湯を出す 「出る」ボタンはロック解除しないと使えない。 ロック設定解除はロック設定ボタン、ロック解除ボ タンによって行う。 

次回までにこの 話題沸騰ポットのビジネス ユースケースを作成してみて ください。 何をアクターにすればよいか、 よく考えてください。 次回はそこからのスタートです。 

