from abc import abstractmethod,ABC

class Payment(ABC):
    def print_slip(self,ammount):
        print('purchase of ammount-',ammount)
    @abstractmethod
    def payment(self,ammount):
        pass
class CreditCardPayment(Payment):
    def payment(self,ammount):
        print('credit card payment is==',ammount)
obj= CreditCardPayment()
obj.payment(100)
obj.print_slip(200)
print(isinstance(obj,Payment))
obj.payment(500)
obj.print_slip(500)
print(isinstance(obj,Payment))

def passKeyword():
  numbers=[100,23,45,178,340,25,67,70,888,900,52]
  for num in numbers:
      if num >100:
          #do nothing
         pass
      else:
          print(num)
passKeyword()