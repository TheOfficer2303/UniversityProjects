#include <iostream>
#include <assert.h>
#include <stdlib.h>
#include <vector>

using namespace std;

class Point {
  public:
    int x;
    int y;
    Point() {}
    Point(int x, int y) {
      x = x;
      y = y;
    }
};

class Shape {
  public:
    virtual void draw()=0;
    virtual void move(Point*)=0;
};

class Circle : public Shape {
  private:
    double radius;
    Point center;
  public:
    Circle() {}
    virtual void draw() {
      std::cerr <<"in drawCircle\n";
    }

    virtual void move(Point* p) {
      center.x += p->x;
      center.y += p->y;
      std::cerr <<"in moveCircle\n";
    }
};

class Rhomb : public Shape {
  private:
    double side;
    Point center;
  public:
    Rhomb() {}
    virtual void draw() {
      std::cerr <<"in drawRhomb\n";
    }

    virtual void move(Point* p) {
      center.x += p->x;
      center.y += p->y;
      std::cerr <<"in moveRhomb\n";
    }
};

class Square : public Shape {
  private:
    double side;
    Point center;
  public:
    Square() {}
    virtual void draw() {
      std::cerr <<"in drawSquare\n";
    }

    virtual void move(Point* p) {
      center.x += p->x;
      center.y += p->y;
      std::cerr <<"in moveSquare\n";
    }
};

void drawShapes(const std::vector<Shape*>& shapes) {
  for (auto shape : shapes) {
    shape->draw();
  }
}

void moveShapes(const std::vector<Shape*>& shapes, Point* p) {
  for (auto shape : shapes) {
    shape->move(p);
  }
}

int main() {
  std::vector<Shape*> shapes;
  shapes.push_back(new Circle());
  shapes.push_back(new Square());
  shapes.push_back(new Square);
  shapes.push_back(new Circle());
  shapes.push_back(new Rhomb());

  drawShapes(shapes);
  moveShapes(shapes, new Point(5, 5));
}
