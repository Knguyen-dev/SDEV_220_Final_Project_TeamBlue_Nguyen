import sqlalchemy as sa

engine = sa.create_engine('sqlite+pysqlite:///PyProject.db', echo=True)

with engine.connect() as conn:

    def GetItems(Items):
        for i in Items:
            print(f"Item: {i[1]}")
        return

    def GetUsers(Users):
        for i in Users:
            print(f"User: {i[1]} {i[2]}")
        return

    def GetOrders(Orders):
        for i in Orders:
            print(f"Total: {i[1]}")
            print(f"User ID: {i[2]}")
        return

    def GetOrderBreakdown(OrderBreakdowns):
        for i in OrderBreakdowns:
            print(f'''Order ID: {i[1]}
                      Item ID: {i[2]}
                      Quantity: {i[3]}''')
        return


    # Create a db if it doesn't exist

    # We'll have to change the default image path later
    conn.execute(sa.text('''
    CREATE TABLE IF NOT EXISTS Items
    (
        id integer primary key,
        name text not null,
        price decimal(6,2) not null,
        description text,
        image text default('/img/scr/')
    );
    '''))

    conn.execute(sa.text('''
    CREATE TABLE IF NOT EXISTS Users
    (
        id integer primary key,
        username text not null,
        fname text not null,
        lname text not null,
        email text not null,
        balance decimal(6,2) default(0.00) not null,
        address text,
        points integer default(0)
    );
    '''))

    conn.execute(sa.text('''
    CREATE TABLE IF NOT EXISTS Orders
    (
        id integer primary key,
        total decimal(6,2) default(0.00) not null,
        user_id integer references Users (id)
    );
    '''))

    conn.execute(sa.text('''
    CREATE TABLE IF NOT EXISTS OrderBreakdown
    (
        id integer primary key,
        order_id integer references Orders (id),
        item_id integer references Items (id),
        quantity integer default(1) not null
    );
    '''))

    conn.commit()

    t = ["Items", "Users", "Orders", "OrderBreakdown"]
    choice = int(input(f"Table choice: 1 {t[0]}, 2 {t[1]}, 3 {t[2]}, 4 {t[3]}"))

    query = sa.text(f"SELECT * FROM {t[choice-1]}")
    rows = conn.execute(query)

    if choice == 1:
        GetItems(rows)
    elif choice == 2:
        GetUsers(rows)
    elif choice == 3:
        GetOrders(rows)
    elif choice == 4:
        GetOrderBreakdown(rows)
