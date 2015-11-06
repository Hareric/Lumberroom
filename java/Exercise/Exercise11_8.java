/*
 * Author = Eric_Chan
 * Create_Time = 2015/11/4
 */
import java.util.Date;
public class Exercise11_8
{
	public static void main(String[] args)
	{
		Account user_1 = new Account(1122,1000,"George");
		user_1.setAnnualInterstRate(0.015);
		user_1.deposit(30, "第一次存钱");
		user_1.deposit(40, "第二次存钱");
		user_1.deposit(50, "第三次存钱");
		user_1.withDraw(5, "第一次取钱");
		user_1.withDraw(4, "第二次取钱");
		user_1.withDraw(2, "第三次取钱");
		System.out.println(user_1.toString());
	}
}



class Account
{
	private int id = 0;
	private double balance = 0;
	private double annualInterestRate = 0; //表示当前利率
	private Date dataCreated = new Date();
	private String name; //记录账户用户名
	private java.util.ArrayList transactions = new java.util.ArrayList(); //记录该账户交易的列表
	
	class Transaction //详细记录每一笔交易的类
	{
		private char type;//记录交易的类型 'W'表示取钱 ; 'D'表示存钱
		private Date date = new Date();//用来记录交易的时间
		private double amount;//记录交易的数额
		private double balance;//剩余的金额
		private String description ;//记录交易的描述
		
		Transaction(char type,double amount,double balance,String description)
		{
			this.type = type;
			this.amount = amount;
			this.balance = balance;
			this.description = description;
		}
		
		public String toString()
		{
			return type + "   |" + date.toString() + "| " + amount +" |   " + balance +"   |" +  description + '\n'; 
		}
	}
	
	
	Account(){		
	}
	
	Account(int id,double balance)
	{
		this.id = id;
		this.balance = balance;
	}
	
	Account(int id,double balance,String name)
	{
		this(id,balance);
		this.name = name;
	}
	
	void setID(int id)
	{
		this.id = id;
	}
	
	int getID()
	{
		return this.id;
	}
	
	void setBalance(double balance)
	{
		this.balance = balance;
	}
	
	double getBalance()
	{
		return this.balance;
	}
	
	void setAnnualInterstRate(double annualInterstRate)
	{
		this.annualInterestRate = annualInterstRate;
	}
	
	double getAnnualInterstRate()
	{
		return this.annualInterestRate;
	}
	
	String getDateCreated() //返回创建该类的时间
	{
		return this.dataCreated.toString();
	}
	
	double getMonthlyInterestRate()//返回月利率
	{
		return this.annualInterestRate / 12 ;
	}
	
	void withDraw(double lessMoney,String description)//取钱
	{
		this.balance -= lessMoney;
		Transaction my_transaction = new Transaction('W' , lessMoney , this.balance ,description);
		this.transactions.add(my_transaction);
	}
	
	void deposit(double addMoney,String description)//存钱
	{
		this.balance += addMoney;
		Transaction my_transaction = new Transaction('D' , addMoney , this.balance ,description);
		this.transactions.add(my_transaction);
	}
	
	public String toString()
	{
		return  "姓名:" + this.name + " 利率:" + this.annualInterestRate + " 收支额:" + this.balance + '\n'
				+ "交易类型 |             交易时间                     |交易的数额|  余额         | 描述\n"
				+ this.transactions.toString();
	}
	
	
}
