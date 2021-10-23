#include "Person.h"
#include <iostream>
const char* Person::getAuthor(){

    return "Yizhong Wang";
}
Person::Person(Sex s, const std::string& n):sex(s),name(n){
    this->father =nullptr;
    this->mother = nullptr;
    this->children = People();
}
Person::~Person(){
//     this->mother->removeChild(this);
//     this->father->removeChild(this);
//     this->removeAllChildren();
}

bool Person::setFather(Person* father){
    if(this->father!= nullptr)
        this->father->removeChild(this);
    this->father = father;
    return true;
}


bool Person::setMother(Person* mother){
    if(this->mother != nullptr)
        this->mother->removeChild(this);
    this->mother = mother;
    mother->addChild(this);
    return true;
}

bool Person::hasChild(const Person* child) const{
    for(int i=0; i<this->children.size();i++){
        if(children[i] == child){
            return true;
        }
    }
    return false;
}
bool Person::addChild(Person* child){
    child->getFather()->removeChild(child);
    child->getMother()->removeChild(child);
    child->setFather(this);
    this->children.push_back(child);
    return true;

}

bool Person::removeChild(Person*child){
    if (child != nullptr){
        for(int i =0; i<getNumChildren();i++){
            if(this->getChild(i) == child) {
                this->children.erase(this->children.begin()+i);
           }
       }
        child->setFather(nullptr);
        child->setMother(nullptr);
        return true;
    }
    return false; 
}

void Person::removeAllChildren(){
    while (getNumChildren() > 0){
        removeChild(getChild(0));
    }
}   

void Person::getAncestors(People& results)const{
    Person* current_person = this->getFather();
    while(current_person != nullptr){
        results.push_back(current_person);
        current_person = current_person->getFather();
    }
    current_person = this->getMother();
    while(current_person != nullptr){
        results.push_back(current_person);
        current_person = current_person->getMother();
    }
    return;
}

void Person::getDescendants(People& results) const{
    if(this->children.size() ==0){
        return;
    }
    for(int i =0;i<getNumChildren();i++){
        Person* current_child = this->getChild(i);
        results.push_back(current_child);
        current_child->getDescendants(results);
    }
}

/**
    Get all siblings of this person.
*/
void Person::getSiblings(People& results) const{
    Person* father = this->getFather();
    for (int i =0; i<father->getNumChildren();i++){
        if(father->getChild(i)!= this){
            results.push_back(father->getChild(i));
        }
    }
}

/**
    Get all cousins of this person in the same generation.
*/
void Person::getCousins(People& results) const{
    Person* father = this->getFather();
    Person* grandFather = father->getFather();
    for(int i =0; i<grandFather->getNumChildren();i++){
        if(grandFather->getChild(i)!=father){
            Person* cousin_parent = grandFather->getChild(i);
            for(int j =0;j<cousin_parent->getNumChildren();j++){
                results.push_back(cousin_parent->getChild(j));
            }
        }
    }
}

