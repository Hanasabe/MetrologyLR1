fn greet(name: &str, age: u32) {
    println!("Hello {}, {}", name, age);
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
    if n == 0 { println!("Zero"); }
    else if n <= 10 { println!("1..10"); }
    else { println!(">10"); }
}

fn main() {
    let name = "Alice";
    let age = 25;

    greet(name, age);

    let mut counter = 5;
    while counter > 0 {
        println!("{}", counter);
        counter -= 1;
    }

    let a = 12;
    let b = 4;

    println!("{}", a + b);
    println!("{}", a - b);
    println!("{}", a * b);
    println!("{}", a / b);
    
    let x = true;
    let y = false;
    println!("{}", x && y);
    println!("{}", x || y);
    println!("{}", !x);

    println!("{}", factorial(6));
    println!("{}", sum_numbers(15));

    number_type(0);
    number_type(5);
    number_type(12);

    if a > 10 && b < 10 {
        println!("Condition met");
    } else {
        println!("Condition not met");
    }

    let max = if a > b { a } else { b };
    println!("{}", max);

    for i in 1..=5 {
        if i % 2 == 0 { continue; }
        println!("{}", i);
    }

    for i in 1..=3 {
        for j in 1..=2 {
            println!("{}", i + j);
        }
    }

    let mut val = 10;
    val += 5;
    val *= 2;
    println!("{}", val);

    let c = a + b * val;
    let d = factorial(3) + sum_numbers(3);
    println!("{}", c + d);

    let flag = (a > b) && (val > 20);
    if flag {
        println!("Flag true");
    } else {
        println!("Flag false");
    }

    let mut n = 0;
    while n < 3 {
        n += 1;
        println!("{}", n);
    }

    let mut i = 0;
    loop {
        i += 1;
        if i > 2 { break; }
        println!("{}", i);
    }

    let arr = [1, 2, 3];
    for x in arr {
        println!("{}", x);
    }
}