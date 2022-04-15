#![allow(dead_code)]

use proc_macro::TokenStream;
use std::io::Write;

use quote::quote;
use syn::{
    parse_macro_input, AttributeArgs, ItemFn, NestedMeta, Token, Type, TypeParamBound, Visibility,
    WhereClause,
};

mod generate;
mod parse;

use crate::ffi::parse::{normalize_function, parse_doc_comments, parse_macro_config};

macro_rules! extract {
    ($value:expr, $pattern:pat => $extracted_value:expr) => {
        match $value {
            $pattern => $extracted_value,
            _ => panic!(concat!(
                stringify!($value),
                " doesn't match ",
                stringify!($pattern)
            )),
        }
    };
}
use crate::ffi::generate::gen_function;
pub(crate) use extract;
use std::{
    collections::HashMap,
    process::{Command, Stdio},
};
use syn::punctuated::Punctuated;

// metadata for each function in a module
pub(crate) struct Function {
    name: String,
    // location of this function in the module tree
    module: Vec<String>,
    // required feature flags to execute function
    features: Vec<String>,
    // plaintext description of the function used to generate documentation
    description: Vec<String>,

    // standard arguments
    arguments: Vec<Argument>,
    // type arguments
    generics: Vec<Generic>,
    // metadata for return type
    ret: Argument,

    // metadata for constructing new types based on existing types or introspection
    derived_types: Vec<Argument>,
    // syn tree for the function's where clause
    where_clause: Option<WhereClause>,
    // TODO: parse into representation
    dispatch: Vec<Dispatch>,
}

pub(crate) struct Dispatch {
    cond: Option<String>,
    prod: HashMap<String, String>,
}

// Metadata for function arguments, derived types and returns.
pub(crate) struct Argument {
    // argument name. Optional for return types
    name: Option<String>,
    // // c type to translate to/from for FFI. Optional for derived types
    // c_type: Option<String>,
    // // RuntimeType expressed in terms of rust types with generics.
    // // Includes various RuntimeType constructors
    // old_rust_type: Option<RuntimeType>,
    // // a list of names in the rust_type that should be considered generics
    // old_generics: Vec<String>,
    rust_type: Type,
    // // type hint- a more abstract type that all potential arguments inherit from
    // hint: Option<String>,
    // plaintext description of the argument used to generate documentation
    description: Vec<String>,
    // // default value for the argument
    // default: Option<()>,
    // // set to true if the argument represents a type
    // is_type: bool,
    // most functions convert c_to_py or py_to_c. Set to true to leave the value as-is
    // an example usage is slice_as_object,
    // //  to prevent the returned AnyObject from getting converted back to python
    // do_not_convert: bool,
    // // when is_type, use this as an example to infer the type
    // example: Option<RuntimeType>
    meta: Vec<NestedMeta>,
}

pub(crate) struct Generic {
    name: String,
    description: Vec<String>,
    bounds: Punctuated<TypeParamBound, Token![+]>,
    meta: Vec<NestedMeta>,
}

pub(crate) fn ffi_impl(attr: TokenStream, item: TokenStream) -> TokenStream {
    let mut item_: TokenStream = item.clone();

    let config = parse_macro_config(parse_macro_input!(attr as AttributeArgs));

    // Parse the function signature
    let ItemFn {
        attrs, vis, sig, ..
    } = parse_macro_input!(item as ItemFn);

    // assert that visibility must be public
    extract!(vis, Visibility::Public(_) => ());

    let doc_comments = parse_doc_comments(attrs);

    let function = normalize_function(sig, doc_comments, config);
    let function_name = function.name.clone();

    let function_item = gen_function(function);

    // current state of the generated function:
    reformat(quote!(#function_item), function_name);

    // for now, just return the base function as-is, without adding the extern fn
    item_.extend(TokenStream::from(quote!(#function_item)));

    item_
}

/// nodemon --exec "cargo build --features untrusted" --watch src --watch opendp_derive -e rs
fn reformat(text: impl std::fmt::Display, name: String) {
    let mut rustfmt = Command::new("rustfmt")
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    write!(rustfmt.stdin.take().unwrap(), "{}", text).unwrap();
    let output = rustfmt.wait_with_output().unwrap();
    let formatted = String::from_utf8(output.stdout).unwrap();

    let mut bat = Command::new("bat")
        .arg("--paging")
        .arg("never")
        .arg("-l")
        .arg("rust")
        .arg("--color=always")
        .arg(format!("--file-name={}", name))
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn()
        .unwrap();
    write!(bat.stdin.take().unwrap(), "{}", formatted).unwrap();
    let output = bat.wait_with_output().unwrap();
    let highlighted = String::from_utf8(output.stdout).unwrap();

    print!("\x1B[2J\x1B[1;1H");
    println!("{}", highlighted)
}
