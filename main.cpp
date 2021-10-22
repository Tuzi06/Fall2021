#include <iostream>
#include "Person.h"
using namespace std;


int main(){
    Person steve(Person::MALE,"steve");
    Person mary(Person::FEMALE,"mary");

    // cout<<steve.setMother(&mary);
    // cout<<steve.getMother()->name<<endl;
}