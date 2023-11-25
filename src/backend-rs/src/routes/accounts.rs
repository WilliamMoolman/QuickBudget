use crate::models::{Account, NewAccount};
use crate::services::accounts;
use crate::services::establish_connection_pg;
use rocket::http::Status;
use rocket::serde::json::Json;

#[post("/", data = "<account>")]
pub fn create_account(account: Json<NewAccount<'_>>) -> Json<Account> {
    let conn = &mut establish_connection_pg();
    Json(accounts::create_account(conn, account.into_inner()))
}

#[get("/")]
pub fn list_accounts() -> Json<Vec<Account>> {
    let conn = &mut establish_connection_pg();
    Json(accounts::list_accounts(conn))
}

#[get("/<id>")]
pub fn get_account(id: i32) -> Result<Json<Account>, Status> {
    let conn = &mut establish_connection_pg();
    match accounts::get_account(conn, id) {
        Some(account) => Ok(Json(account)),
        None => Err(Status::NotFound),
    }
}

#[put("/<id>", data = "<account>")]
pub fn update_account(id: i32, account: Json<Account>) -> Json<String> {
    let conn = &mut establish_connection_pg();
    match accounts::update_account(conn, id, account.into_inner()) {
        Ok(_) => Json(String::from("Account updated successfully")),
        Err(_) => Json(String::from("Failed to update account")),
    }
}

#[delete("/<id>")]
pub fn delete_account(id: i32) -> Json<String> {
    let conn = &mut establish_connection_pg();
    match accounts::delete_account(conn, id) {
        Ok(_) => Json(String::from("Account deleted successfully")),
        Err(_) => Json(String::from("Failed to delete account")),
    }
}
