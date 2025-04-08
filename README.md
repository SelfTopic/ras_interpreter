# RAS Interpreter

Интерпретатор языка RAS изучает код по каждому символу. Весь код на RAS подразделяется на 3 группы:

    1. Кейворды.
    Ключевые слова, зарегистрированные в языке RAS, такие как local, cl, void и тд.
    
    2. Операторы.
        Вспомогательные знаки, таке как <>, : и тд.
    
    3. Имена.
    Все слова, вводимые программистом. Имена переменных, типов, классов, функций и тд.

    


1. Кейворды

    Список кейвордов RAS:\
    local - создание локальной переменной. Синтаксис: 
        
        local nameVar :type: << value #

    global - создание глобальной переменной. Глобальные переменные можно использовать в других файлах. Синатксис: 

        global nameVar :type: << value #

    im - импорт глобальных имен

        im filename--name, filename--name2

    fn - создание функции. Синтаксис: 
        
        fn nameFunction < param1:type: ++ param2:type: ::
            # код функции
            >> 0 #
        ::

    cl - создание класса. Синтаксис: 

        cl ClassName ::
            param :type: #
        ::

    for - описание итерирования объектов. Синтаксис:

        for number << array ::
            print: number #
        ::

    whi - описание цикла с условием

        whi :true: ::
            print: "Hello, World: #
        ::

    con - логическое если, начало условия, первое условие

        local var :integer: << 10 #

        con :var == 10: ::
            print: "var = 10" #
        ::

    elcon - логическое иначе если, множественное условие, парное с con

        local var :integer: << 10 #

        con :var == 10: ::
            print: "var = 10" #

        :: elcon :var < 10: ::
            print: "var < 10" #

        :: elcon :var > 10: ::
            print: "var > 10" #

        ::

    noc - логическое иначе, последнее условие, парное с con 

        local var :integer: << 10 #

        con :var == 10: ::
            print: "var = 10" #

        :: elcon :var < 10: ::
            print: "var < 10" #

        :: elcon :var > 10: ::
            print: "var > 10" #

        :: noc ::
            print: "var вообще непонятно что" #

        ::


    initialize - метод класса, вызываемый при инициализации класса 

        cl ClassName ::
            param :type: # 

            initialize < data :type: ::
                param << data #
            ::
        ::

    Init - инициализация класса 

        cl ClassName ::
            param :type: # 

            initialize < data :type: ::
                param << data #
            ::
        ::

        local className :ClassName: << Init <10> ClassName # 

    get - геттер для аттрибута класса

        cl ClassName ::
            param :type: # 

            initialize < data :type: ::
                param << data #
            ::

            get param < ::
                print: "Get data" #
                >> param
            ::
        ::

        # использование геттера

        local className :ClassName: << Init <10> ClassName #
        local paramVar :type: << className--param: #

    set - сеттер для аттрибута класса

        cl ClassName ::
            param :type: # 

            initialize < data :type: ::
                param << data #
            ::

            set param < newParam ::
                print: "Set data" #
                param << newParam #
            ::
        ::

        # использование сеттера

        local className :ClassName: << Init <10> ClassName #
        local varParam :type: << 10 #
        className--param << varParam #

    Вызов функции.
        Чтобы вызвать функцию, нужно обратиться к оператору вызова : и передать через запятую аргументы

        local nameVar :integer: << plus: 2, 3 #

    
    
2. Операторы

    в RAS используется много различных операторов.
    
    << - присваивание

        local nameVar :integer: << 10 #

    возвращение из функции

        void nameFunction < param1:type: ++ param2:type: ::
                >> 0 # operator >>
        ::

    :: - оператор сохранения тела. Нужен чтобы описывать тело функции, класса и тд

        void nameFunction < param1:type: ++ param2:type: ::
                >> 0 #
        ::

    : - оператор вызова функции

        local nameVar :integer: << plus: 2, 3 #

    : : - парный :, оператор сохранения условия и типа. Нужен для обьявления типа или для сохранения условия

        local var :integer: << 4 # type

        whi :var > 4: :: #condition
            var << var-1 #
        ::

    < - объявление аргументов функции

        void nameFunction < param1:type: ++ param2:type: ::
                >> 0 #
        ::

    < > - парный тег, оператор создания массива
    !< > - создание кортежа
    ~< > - создание словаря

        local var :list: << <0, 1, 2> # 
        local var :tuple: << !<0, 1, 2> #
        local var :dict: << ~<
            "key" > "value",
            "key2" > "value"
        > #

    оператор окончания строки. он же и комментарий

        #

3 Типы данных

    Зарегистрированные типы данных в RAS

    integer - целое число
    float - дробное число
    string - строка
    empty - ничего
    list - изменяемый массив
    tuple - неизменяемый массив
    dict - массив, хранящий данные в формате ключ > значение