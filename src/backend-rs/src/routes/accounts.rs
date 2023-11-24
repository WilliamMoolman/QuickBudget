use crate::models::{Account, NewAccount};
use crate::services::accounts::{create_account, get_account, get_accounts};
use crate::services::establish_connection_pg;
use rocket::http::Status;
use rocket::serde::json::Json;

#[post("/", data = "<account>")]
pub fn add_account(account: Json<NewAccount<'_>>) -> Json<Account> {
    let conn = &mut establish_connection_pg();
    Json(create_account(conn, account.into_inner()))
}

#[get("/")]
pub fn fetch_accounts() -> Json<Vec<Account>> {
    let conn = &mut establish_connection_pg();
    Json(get_accounts(conn))
}

#[get("/<id>")]
pub fn fetch_account(id: i32) -> Result<Json<Account>, Status> {
    let conn = &mut establish_connection_pg();
    match get_account(conn, id) {
        Some(account) => Ok(Json(account)),
        None => Err(Status::NotFound),
    }
}
