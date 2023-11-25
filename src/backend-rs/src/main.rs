#[macro_use]
extern crate rocket;
use rocket::serde::json::{json, Value};

pub mod models;
pub mod routes;
pub mod schema;
pub mod services;

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[catch(404)]
fn not_found() -> Value {
    json!({
        "status": "error",
        "reason": "Resource was not found."
    })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![index])
        .mount(
            "/accounts",
            routes![
                routes::accounts::create_account,
                routes::accounts::list_accounts,
                routes::accounts::get_account,
                routes::accounts::update_account,
                routes::accounts::delete_account,
            ],
        )
        .register("/", catchers![not_found])
}
