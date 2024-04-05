import mel_parser


def main():
    sql_query1 = '''
            SELECT SUM(salary), name FROM employees WHERE department = 'IT' GROUP BY department
            HAVING COUNT(*) > 1
            ORDER BY salary
        '''
    sql_query2 = '''
            SELECT *, (SELECT MAX(salary) FROM employees) AS max_salary FROM employees WHERE department = 'IT'
        '''
    # prog = mel_parser.parse('''
    #     SELECT a + 5 AS v1,
    #            b
    #       FROM table1
    #         WHERE a + 5 * b > r AND r = 8
    # ''')
    prog1 = mel_parser.parse(sql_query2)
    tree = prog1.tree
    print(*prog1.tree, sep='\n')


if __name__ == "__main__":
    main()
