import pymysql

"""
테이블 생성할때 이거 주석 제거하기 
"""
# 연결
# conn = pymysql.connect(host="rds.t-seonghun.net",
#                             user='root', 
#                             password="Pa$$w0rd", 
#                             db='test', 
#                             charset='utf8')
# cur = conn.cursor()

# 테이블 데이터 추가
# sql = "INSERT INTO test2 (name, phone) VALUES (%s, %s)"

# with conn:
#     with conn.cursor() as cur:
#         cur.execute(sql, ('name1', '010-1111-1111'))
#         cur.execute(sql, ('name2', '010-2222-2222'))
#         conn.commit()

# 데이터 조회
# sql = "SELECT * FROM test2 ORDER BY name"
# with conn:
#     with conn.cursor() as cur:
#         cur.execute(sql)
#         result = cur.fetchall()
#         for data in result:
#             print(data)

# 테이블 생성 
# table = """CREATE TABLE test2(
#             name VARCHAR(100) NOT NULL,
#             phone VARCHAR(100) NOT NULL
#             )"""

# 테이블 조회
# table = 'SHOW TABLES'
# with conn:
#     with conn.cursor() as cur:
#         cur.execute(table)
#         # conn.commit
#         for data in cur:
#             print(data)







    
# 데이터 추가 함수 (이름, 전화번호)
# def InsertData(name,phone):
#     conn = pymysql.connect(host="rds.t-seonghun.net", user='root', password="Pa$$w0rd", db='test', charset='utf8')
#     cur = conn.cursor()

#     cur.execute(f"INSERT INTO test2 (name,phone) VALUES ('{name}','{phone}');")

#     conn.commit()
#     conn.close()





# 테이블값 저장
class Guest_info:
    def __init__(self, name=None, phone=None):
        self.name = name
        self.phone = phone

    def __str__(self):
        return 'name:' + self.name +' / phone:' + self.phone

# 테이블에 관련된 db 작업
class Guest_db:
    def __init__(self):
        # self.conn = None            # 연결된 객체 담을 멤버 변수

        self.conn = pymysql.connect(host="rds.t-seonghun.net", 
                            user='root', 
                            password="Pa$$w0rd", 
                            db='test', 
                            charset='utf8')

    # db 연결 
    # def connect(self):
    #     self.conn = pymysql.connect(host="rds.t-seonghun.net", 
    #                                 user='root', 
    #                                 password="Pa$$w0rd", 
    #                                 db='test', 
    #                                 charset='utf8')
    
    def disconnect(self):
        self.conn.close()

    # 데이터 추가 함수 (이름, 전화번호)
    def InsertData(self, name, phone):
        # self.connect()
        cur = self.conn.cursor()

        sql = "INSERT INTO test2 (name, phone) VALUES (%s, %s)"        # 변수가 들어갈 위치에 포맷문자로 지정

        vals = (name, phone)
        cur.execute(sql, vals)

        self.conn.commit()
        # self.disconnect()
        cur.close()

    def select(self, name):
        # self.connect()             # db연결
        cur = self.conn.cursor()

        sql = "SELECT * FROM test2 where name=%s"
        vals = (name,)

        cur.execute(sql,vals)           # 쿼리 실행 , 검색 결과가 cur 에 저장 
        row = cur.fetchone()            # cur 객체에서 검색된 한줄 fetch, 검색 결과 없으면 None 볌환

        # self.disconnect()
        cur.close()


        if row!= None:                               # 검색된 결과가 있으면
            info = Guest_info(row[0], row[1])
            return info 

    def update(self, name, new_phone):
        # self.connect()             # db연결
        cur = self.conn.cursor()

        sql = "UPDATA MEMBER SET PHONE=%s WHERE ID=%s"
        vals = (new_phone, name)
        cur.execute(sql,vals)           # 쿼리 실행 , 검색 결과가 cur 에 저장 
        self.conn.commit()
        # self.disconnect()
        cur.close()


    def delete(self, name):
        # self.connect()             # db연결
        cur = self.conn.cursor()

        sql = "DELETE FROM MEMBER WHERE name=%s"
        vals = (name,)
        cur.execute(sql, vals)
        self.conn.commit()
        # self.disconnect()
        cur.close()



# # class Service:
#     '''
#     로그인 상태 유지 —> 로그인 함수에서 처리한 아이디 보관
#     로그인함수() : 이름, 전화번호 입력받아 데이터베이스랑 일치하는가 확인 —> 로그인 성공
#     기억상실처리 -> 로그인에 성공한 이름을 저장, 로그아웃 할때까지 유지
#     '''


