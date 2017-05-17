using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Net;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Net.Sockets;
using System.Windows.Forms;
using System.Threading;
using System.IO;
using System.Security.Cryptography;

namespace teacher_gui_windows_forms
{
    class SessionWithServer
    {
        private int localPort = 1027;
        private int localStreamPort = 1028;
        private string localHost = "127.0.0.1";
        private TeacherGUI form;
        public Socket guiCommandSocket;
        public Socket guiStreamSocket;
        public Socket streamSocket;
        public Socket commandSocket;

        public SessionWithServer(TeacherGUI form)
        {
            ///<summary>
            ///The structive function.
            ///</summary>
            ///<param name="form">The GUI.</param>
            this.form = form;
            this.form.ListView1.SmallImageList = this.form.ImageList1;

            IPEndPoint commandIPEndPoint = new IPEndPoint(IPAddress.Parse(localHost), localPort);
            guiCommandSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            guiCommandSocket.Bind(commandIPEndPoint);
            guiCommandSocket.Listen(1);

            IPEndPoint streamIPEndPoint = new IPEndPoint(IPAddress.Parse(localHost), localStreamPort);
            guiStreamSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            guiStreamSocket.Bind(streamIPEndPoint);
            guiStreamSocket.Listen(1);

            Console.WriteLine("waiting fot command socket to connect");
            commandSocket = guiCommandSocket.Accept();
            Console.WriteLine("command socket accepted");


            Thread waitingFotClients = new Thread(new ThreadStart(AddClient));
            waitingFotClients.Start();
            Console.WriteLine("Thread started");
        }

        public void AddListItemMethod(string ip)
        {
            ListViewItem listImage = new ListViewItem(ip, form.ImageList1.Images.Count - 1);
            form.ListView1.Items.Add(listImage);
            listImage.ImageKey = ip;
            form.ListView1.Update();
        }

        public void AddClient()
        {
            ///<summary>
            ///A function for a Threads.
            ///The streamSocket waits for a new client to connect.
            ///Connects another client with the server for stream.
            ///And starts the stream for the client with a thread.
            ///</summary>
            ///<returns>Void</returns>

            byte[] clientIP = new byte[32];

            while (true)
            {
                Console.WriteLine("waiting for client");
                streamSocket = guiStreamSocket.Accept();
                Console.WriteLine("client accepted");

                streamSocket.Receive(clientIP);
                string stringIP = Encoding.Default.GetString(clientIP);
                Console.WriteLine("got client's ip: " + stringIP);

                Thread.Sleep(50);
                AddImage(stringIP);

                ForStream SocketToUse = new ForStream(streamSocket, this);
                Thread stream = new Thread(new ThreadStart(SocketToUse.GetStream));
                stream.Start();
            }
        }

        public Image GetAnImage()
        {
            byte[] lenOfImage = new byte[7];
            byte[] temporaryData = new byte[1024];
            byte[] encodedImg = new byte[0];
            int bytesReceived = 0;

            streamSocket.Receive(lenOfImage, 0, 7, SocketFlags.None);
            int imageLength = Convert.ToInt32(Encoding.Default.GetString(lenOfImage));
            Array.Resize(ref encodedImg, imageLength);
            while (bytesReceived < imageLength)
            {
                bytesReceived += streamSocket.Receive(encodedImg, bytesReceived, Math.Min(1024, imageLength - bytesReceived), SocketFlags.None);
            }

            //Console.WriteLine(Encoding.Default.GetString(encodedImg));
            //byte[] decodedImg = new byte[bytesReceived];
            //FromBase64Transform transfer = new FromBase64Transform();
            //transfer.TransformBlock(encodedImg, 0, bytesReceived, decodedImg, 0);
            //Console.WriteLine(decodedImg.Length);
            //Console.WriteLine(Encoding.Default.GetString(decodedImg));
            using (var ms = new MemoryStream(encodedImg))
            {
                return Image.FromStream(ms);
            }
        }

        public void AddImage(string ip)
         {
            ///<summary>
            ///When a new client is added his image is added
            ///to the ImageList thus appear on the gui.
            ///</summary>
            ///<param name="ip">An ip of a client in string.</param>
            ///<returns>Void</returns>
            Console.WriteLine("adding image");
            Image image = GetAnImage();
            form.ImageList1.Images.Add(ip, image);
            form.ListView1.Invoke(new MethodInvoker(delegate
            {
                AddListItemMethod(ip);
            }));
        }

        public void ChangeImage(Image image, string ip)
        {
            ///<summary>
            ///Whenever a new image is received, this function changes the client's image to the current image.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<param name="ip">Am ip of a client.</param>
            ///<returns>Void</returns>
            int i = 0;
            form.ListView1.Invoke(new MethodInvoker(delegate
            {
                foreach (ListViewItem item in form.ListView1.Items)
                {
                    if (item.Text.Equals(ip))
                    {
                        form.ImageList1.Images[i] = image;
                        item.ImageIndex = i;
                        form.ListView1.Refresh();
                        break;
                    }
                    i++;
                }
            }));
        }

    }

    class ForStream
    {
        //This class if for the thread get stream to use.
        Socket streamSocket;
        SessionWithServer mainClass;

        public ForStream(Socket streamSocket, SessionWithServer mainClass)
        {
            this.streamSocket = streamSocket;
            this.mainClass = mainClass;
        }

        public void GetStream()
        {
            byte[] clientIP = new byte[32];
            while (true)
            {
                streamSocket.Receive(clientIP);
                Image img = mainClass.GetAnImage();
                mainClass.ChangeImage(img, Encoding.Default.GetString(clientIP));
            }
        }
    }
}
