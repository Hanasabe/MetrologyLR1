use std::io;

fn greet(name: &str, age: u32) {
    println!("Hello, my name is {} and I am {} years old.", name, age);
}

fn is_adult(age: u32) -> bool {
    age >= 18
}

fn factorial(n: u32) -> u32 {
    if n <= 1 { 1 } else { n * factorial(n - 1) }
}

fn sum_numbers(n: u32) -> u32 {
    let mut sum = 0;
    for i in 1..=n {
        sum += i;
    }
    sum
}

fn number_type(n: i32) {
    match n {
        0 => println!("Number is zero"),
        1..=10 => println!("Number between 1 and 10"),
        _ => println!("Number greater than 10 or negative"),
    }
}

fn main() {
    let mut input = String::new();
    println!("Enter your name:");
    io::stdin().read_line(&mut input).expect("Failed to read line");
    let name = input.trim();

    input.clear();
    println!("Enter your age:");
    io::stdin().read_line(&mut input).expect("Failed to read line");
    let age: u32 = input.trim().parse().expect("Type a number!");

    greet(name, age);

    if is_adult(age) {
        println!("You are an adult.");
    } else {
        println!("You are not an adult.");
    }

    let mut counter = 5;
    while counter > 0 {
        println!("Countdown: {}", counter);
        counter -= 1;
    }

    let mut i = 0;
    loop {
        i += 1;
        if i > 3 { break; }
        println!("Loop iteration {}", i);
    }

    let a = 12;
    let b = 4;
    println!("{} + {} = {}", a, b, a + b);
    println!("{} - {} = {}", a, b, a - b);
    println!("{} * {} = {}", a, b, a * b);
    println!("{} / {} = {}", a, b, a / b);
    println!("{} % {} = {}", a, b, a % b);

    let x = true;
    let y = false;
    println!("x AND y = {}", x && y);
    println!("x OR y = {}", x || y);
    println!("NOT x = {}", !x);

    let numbers = [1, 2, 3, 4, 5];
    for num in numbers.iter() {
        println!("Array number: {}", num);
    }

    let mut vec = vec![10, 20, 30];
    vec.push(40);
    println!("Vector: {:?}", vec);

    println!("Factorial of 6: {}", factorial(6));
    println!("Sum 1 to 15: {}", sum_numbers(15));

    number_type(0);
    number_type(5);
    number_type(12);

    if a > 10 && b < 10 {
        println!("Condition met: a > 10 AND b < 10");
    } else {
        println!("Condition not met");
    }

    let max = if a > b { a } else { b };
    println!("Max of {} and {} is {}", a, b, max);

    let tup = ("Rust", 2026, true);
    let (lang, year, active) = tup;
    println!("Language: {}, Year: {}, Active: {}", lang, year, active);

    for i in 1..=5 {
        if i % 2 == 0 { continue; }
        println!("Odd number: {}", i);
    }

    {
        let nested = "Inside nested block";
        println!("{}", nested);
    }

    for i in 1..=3 {
        for j in 1..=2 {
            println!("i={}, j={}", i, j);
        }
    }

    let mut val = 10;
    val += 5;
    val *= 2;
    println!("Result after operations: {}", val);
}