use super::schema::accounts;
use diesel::prelude::*;
extern crate rocket;
use rocket::serde::{Deserialize, Serialize};

#[derive(Queryable, Selectable, Serialize, Deserialize, AsChangeset)]
#[serde(crate = "rocket::serde")]
#[diesel(table_name = crate::schema::accounts)]
#[diesel(check_for_backend(diesel::pg::Pg))]
pub struct Account {
    pub id: i32,
    pub name: String,
    pub balance: i32,
    pub active: bool,
}

#[derive(Insertable, Deserialize, Serialize)]
#[serde(crate = "rocket::serde")]
#[diesel(table_name = accounts)]
pub struct NewAccount<'a> {
    pub name: &'a str,
    pub balance: i32,
}
