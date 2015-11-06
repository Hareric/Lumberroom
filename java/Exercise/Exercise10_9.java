package ch10;
/*
 * Author = Eric_Chan
 * Create_Time = 2015/10/22
 */
public class Exercise10_9 {
	public static void main(String[] args)
	{
		Course courseMath = new Course("Math");
		courseMath.addStudent("Vincent");
		courseMath.addStudent("Sponge");
		courseMath.addStudent("Eric");
		System.out.println(courseMath.toString());
		
		courseMath.dropStudent("Sponge");
		System.out.println(courseMath.toString());
		courseMath.clear();
	}
	

}

class Course
{
	private String courseName;
	private int numOfStudent = 0; //用来记录当前学生的人数
	private int n = 20;//当前学生数组的大小
	private String[] students = new String[n];
	
	public Course(String courseName)
	{
		this.courseName = courseName;
	}
	
	public void addStudent(String studentName)//为学生数组添加新学生
	{
		this.students[numOfStudent] = studentName;
		numOfStudent++;
		
		if(numOfStudent == n)//若学生数组满了 自动进行扩张
		{
			n += 20;
			String[] students = new String[n];
			for(int i=0;i<numOfStudent;i++)
				students[i] = this.students[i];
			this.students = students;
		}
	}
	
	public String[] getStudents()
	{
		return this.students;
	}
	
	public int getNumOfStudent()
	{
		return this.numOfStudent;
	}
	
	public String getCourseName()
	{
		return this.courseName;
	}
	
	public void dropStudent(String student)
	{
		String[] temp_students = new String[this.n];
		int numOfStudent=this.numOfStudent;
		for(int i=0,j=0;i<this.numOfStudent;i++)
		{
			
			if (this.students[i].equals(student))
			{
				numOfStudent--;
				continue;
			}
			else
			{
				temp_students[j++] = this.students[i];
			}
				
		}
		this.students = temp_students;
		this.numOfStudent = numOfStudent;
	}
	
	public void clear()
	{
		this.students = new String[n];
		this.numOfStudent = 0;
	}
	
	public String toString()
	{
		String returnString = "";
		returnString += "科目：" + this.courseName + '\n' + "现有学生人数:" + this.numOfStudent + '\n';
		returnString += "学生名单\n";
		for(int i=0;i<this.numOfStudent;i++)
			returnString += (this.students[i] + " ");	
		return returnString;
	}	
}
