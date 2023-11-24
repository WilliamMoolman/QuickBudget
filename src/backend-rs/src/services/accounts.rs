use crate::models::{Account, NewAccount};
use diesel::pg::PgConnection;
use diesel::prelude::*;

pub fn create_account(conn: &mut PgConnection, new_account: NewAccount) -> Account {
    use crate::schema::accounts;

    diesel::insert_into(accounts::table)
        .values(&new_account)
        .returning(Account::as_returning())
        .get_result(conn)
        .expect("Error saving new account")
}

pub fn get_accounts(conn: &mut PgConnection) -> Vec<Account> {
    use crate::schema::accounts::dsl::*;
    accounts
        .select(Account::as_select())
        .load(conn)
        .expect("Error loading posts")
}

pub fn get_account(conn: &mut PgConnection, id: i32) -> Option<Account> {
    use crate::schema::accounts::dsl::accounts;

    accounts
        .find(id)
        .select(Account::as_select())
        .first(conn)
        .optional()
        .expect("Error getting account") // This allows for returning an Option<Post>, otherwise it will throw an error
}
