// @generated automatically by Diesel CLI.

diesel::table! {
    accounts (id) {
        id -> Int4,
        name -> Varchar,
        balance -> Int4,
        active -> Bool,
    }
}

diesel::allow_tables_to_appear_in_same_query!(accounts,);
