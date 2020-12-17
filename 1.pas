{ # 17 > PART1 may be numeral of any SCALE }
FUNCTION AMONG_NUMERALS (PART : STR95;
        {==============} VAR ERC : INTEGER) : SCALE;
CONST
  MAXUNUS = 3;
  UNUSW : ARRAY [1..MAXUNUS] OF STR7 =  ('ОДИН','ОДНА','ОДНО');
  MAXSMALL = 8;
  SMALLW : ARRAY [1..MAXSMALL] OF STR7 = ('ДВА','ДВЕ','ОБА','ОБЕ','ПОЛТОРА','ПОЛТОРЫ','ТРИ','ЧЕТЫРЕ');
  MAXBIG1 = 9;
  BIGW1 : ARRAY [1..MAXBIG1] OF STRING [13] = ('ДВОЕ','ТРОЕ','ЧЕТВЕРО','ПЯТЕРО','ШЕСТЕРО','СЕМЕРО','ВОСЬМЕРО','ДЕВЯТЕРО','ДЕСЯТЕРО');
  MAXBIG2 = 39;
  BIGW2 : ARRAY [1..MAXBIG2] OF STRING [13] = ('ПЯТЬ','ШЕСТЬ','СЕМЬ','ВОСЕМЬ','ДЕВЯТЬ','ДЕСЯТЬ','ОДИННАДЦАТЬ','ДВЕНАДЦАТЬ','ТРИНАДЦАТЬ','ЧЕТЫРНАДЦАТЬ','ПЯТНАДЦАТЬ','ШЕСТНАДЦАТЬ','СЕМНАДЦАТЬ','ВОСЕМНАДЦАТЬ','ДЕВЯТНАДЦАТЬ','ДВАДЦАТЬ','ТРИДЦАТЬ','ТРИДЕВЯТЬ','СОРОК','ПЯТЬДЕСЯТ','ШЕСТЬДЕСЯТ','СЕМЬДЕСЯТ','ВОСЕМЬДЕСЯТ','ДЕВЯНОСТО','ДВЕСТИ','СТО','ПОЛСТА','ПОЛТОРАСТА','ТРИСТА','ЧЕТЫРЕСТА','ПЯТЬСОТ','ШЕСТЬСОТ','СЕМЬСОТ','ВОСЕМЬСОТ','ДЕВЯТЬСОТ','СКОЛЬКО','НЕМАЛО','НЕСКОЛЬКО','МНОГО');
VAR
  I, NUM : INTEGER;
  SCL : SCALE;
  FOUND : BOOLEAN;
BEGIN
  VAL (PART, NUM, ERC);
  IF ERC = 0
    THEN
      BEGIN
        IF ((NUM MOD 100) DIV 10 = 1)
          THEN SCL := BIG2
          ELSE
            CASE (NUM MOD 10) OF
              1 : SCL := UNUS;
              2, 3, 4 : SCL := SMALL;
              0, 5, 6, 7, 8, 9 : SCL := BIG2;
            END;
      END;
  ELSE 
    BEGIN
      I := 0;
      REPEAT
        INC(I);
        FOUND := (PART = UNUSW[I]);
      UNTIL FOUND OR (I = MAXUNUS);
      IF FOUND 
        THEN SCL := UNUS
        ELSE
          BEGIN
            I := 0;
            REPEAT
              INC(I);
              FOUND := (PART = SMALLW[I]);
            UNTIL FOUND OR (I = MAXSMALL);
            IF FOUND 
              THEN SCL := SMALL
                ELSE
                  BEGIN
                    I := 0;
                    REPEAT
                      INC(I);
                      FOUND := (PART = BIGW1[I]);
                    UNTIL FOUND OR (I = MAXBIG1);
                    IF FOUND 
                      THEN SCL := BIG1
                      ELSE
                        BEGIN
                          I := 0;
                          REPEAT
                            INC(I);
                            FOUND := (PART = BIGW2[I]);
                          UNTIL FOUND OR (I = MAXBIG2);
                          IF FOUND 
                            THEN SCL := BIG2
                            ELSE SCL := NOTNUM;
                        END;
                  END;
          END;
    END;
  AMONG_NUMERALS := SCL;
END.