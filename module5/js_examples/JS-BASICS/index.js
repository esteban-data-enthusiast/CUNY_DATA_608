//constant
const interestRate = 0.3;
//interestRate = 1;
console.log(interestRate);


let name = 'Esteban'; // String literal
let age = 40;         // Number Literal
let isApproved = false; // Boolean Literal
let firstName  = undefined;
let lastName = null;  // null to explicitly clear the value of a variable

// declare object
let person = {
    name: 'Esteban',
    age: 30
};

console.log(person);

// Dot notation
person.name = 'John';
console.log(person.name);

// Bracket notation
person['name'] = 'Mary';
console.log(person['name']);
let selection = 'name';
person[selection] = 'Mario';
console.log(person[selection]);


// Array (it is an object) to represent a list of items
let selectedColors = ['red','blue'];
console.log(selectedColors);
// Exapnd array (length is dynamic)
selectedColors[2] = 'green';
console.log(selectedColors);
// Expand array with a numeric value (array can dynamically store multiple types)
selectedColors[3] = 1.5;
console.log(selectedColors);


// declare function that performs a task and takes a parameter 'name'
function greet(name) {
    console.log('Hello ' + name);
}
// call function passing argument 'Tom'
greet('Tom');
// call function passing argument 'Mary'
greet('Mary');


// declare function that calculates and returns a value
function square(number) {
    return number * number;
}
// call square function
console.log(square(6));
console.log(square(9));