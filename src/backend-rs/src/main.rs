#[macro_use]
extern crate rocket;

pub mod models;
pub mod routes;
pub mod schema;
pub mod services;

#[get("/")]
fn index() -> &'static str {
    "Hello, world!"
}

#[launch]
fn rocket() -> _ {
    rocket::build().mount("/", routes![index]).mount(
        "/accounts",
        routes![
            routes::accounts::add_account,
            routes::accounts::fetch_accounts,
            routes::accounts::fetch_account,
        ],
    )
}
