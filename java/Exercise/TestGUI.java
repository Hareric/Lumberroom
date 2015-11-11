package ch12;
/*
 * Author = Eric_Chan
 * Create_Time = 2015/11/9
 */

import javax.swing.*;
import java.awt.*;
public class TestGUI extends JFrame{
	//javax.swing.ImageIcon 创建一个图片的对象,可用做按钮
	private ImageIcon qitiandasheng = new ImageIcon("sorce/picture/qitiandasheng.jpg");

	TestGUI()
	{
		JPanel p1 = new JPanel();
		p1.setLayout(new GridLayout(4,3));
		//java.awt.Color 类内包含了 默认设置的颜色,也可以自定义类设置rgb定义新的颜色
		Color[] color = {Color.red,Color.blue,Color.black,Color.cyan,Color.darkGray,new Color(255,0,156)};
		for(int i=1;i<=9;i++)
		{
			JButton temp = new JButton(""+i);
			temp.setBackground(color[i%6]);
			temp.setForeground(color[(i+2)%6]);
			p1.add(temp);
		}
		
		p1.add(new JButton(""+0));
		p1.add(new JButton("Start"));
		p1.add(new JButton("Stop"));
		
		JPanel p2 = new JPanel(new BorderLayout());
		p2.add(new JTextField("孙 悟 空"),BorderLayout.NORTH);
		p2.add(p1,BorderLayout.CENTER);
	    
		add(p2,BorderLayout.EAST);
		//java.awt.Font 类创建一种字体 public Font(String 字体名,int 字体风格,int 字体大小)
		//字体:SansSerif  Serif  Monospaced  Dialog  DialogInput
		//字体风格:Font.PLAIN  Font.BLOD  Font.ITALIC  Font.BOLD + Font.ITALIC
		Font font1 = new Font("Dialog",Font.BOLD+Font.ITALIC,15);
		JButton temp = new JButton("齐 天 大 圣");
		temp.setFont(font1);
		temp.setBackground(color[4]);
		temp.setForeground(color[2]);
		add(temp,BorderLayout.WEST);
		add(new JButton(this.qitiandasheng),BorderLayout.CENTER);
		
	}
	
	public static void main(String[] args)
	{
		TestGUI frame = new TestGUI();
        frame.setTitle("The front view of a Microwave ovean");
        frame.setSize(800,350);    
        frame.setLocationRelativeTo(null); 
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setBackground(Color.red);
        frame.setVisible(true);      
	}
}
