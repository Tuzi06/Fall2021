#include <iostream>
#include "Person.h"
using namespace std;


int main(){
    cout<<"start"<<endl;
    Person steve(Person::MALE,"steve");
    // cout<<steve.getMother()<<endl;
    Person mary(Person::FEMALE,"mary");
    // cout<<"start"<<endl;
    cout<<steve.setMother(&mary);
    // cout<<"start"<<endl;
    // cout<<steve.getMother()->name<<endl;
    cout<<mary.removeChild(&steve)<<endl;
    return 0;
}