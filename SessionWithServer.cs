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

namespace teacher_gui_windows_forms
{
    class SessionWithServer
    {
        private int localPort = 1027;
        private string localHost = "127.0.0.1";
        private TeacherGUI form;
        private Socket mainSocket;

        public SessionWithServer(TeacherGUI form)
        {
            ///<summary>
            ///The structive function.
            ///</summary>
            ///<param name="form">The GUI..</param>
            mainSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            mainSocket.Connect(localHost, localPort);
            this.form = form;
        }

        public void AddClient()
        {
            ///<summary>
            ///Connects another socket for another client with the server.
            ///Adds the socket to the clientsSockets.
            ///</summary>
            ///<returns>Void</returns>
            IPEndPoint IPAndPort = new IPEndPoint(Convert.ToInt64(localHost), localPort);
            UdpClient thisComputer = new UdpClient(IPAndPort);
            IPEndPoint sender = new IPEndPoint(IPAddress.Any, localPort);
            byte[] lenOfImg = new byte[7];

            thisComputer.Receive(ref sender);
            thisComputer.Connect(sender);

            lenOfImg = thisComputer.Receive(ref sender);
            AddImage(thisComputer, sender);
            ForStream SocketToUse = new ForStream(thisComputer, this);
            Thread stream = new Thread(new ThreadStart(SocketToUse.GetStream));
            stream.Start();
        }

        public Image GetAnImage(UdpClient thisComputer, IPEndPoint client)
        {
            byte[] lenOfImage = new byte[7];
            byte[] temperoryData = new byte[1024];
            byte[] encodedImg = new byte[0];
            int offsetOfBuffer = 0;

            lenOfImage = thisComputer.Receive(ref client);
            Array.Resize(ref encodedImg, BitConverter.ToInt32(lenOfImage, 0));
            temperoryData = thisComputer.Receive(ref client);
            for(int i=offsetOfBuffer; i<offsetOfBuffer+1024; i++)
            {
                encodedImg[i] = temperoryData[i];
            }
            offsetOfBuffer += 1024;
            int lengthOfImg = BitConverter.ToInt32(encodedImg, 0);

            while (encodedImg.Length + 1024 < lengthOfImg)
            {
                thisComputer.Receive(encodedImg, offsetOfBuffer, 1024, SocketFlags.None);
                offsetOfBuffer += 1024;
                lengthOfImg = BitConverter.ToInt32(encodedImg, 0);
            }

            thisComputer.Receive(encodedImg, offsetOfBuffer, BitConverter.ToInt32(encodedImg, 0) - lengthOfImg, SocketFlags.None);
            byte[] decodedImg = Convert.FromBase64String(Encoding.Default.GetString(encodedImg));
            Image img = ConvertByteArrayToImage(decodedImg);
            return img;
        }

        private Image ConvertByteArrayToImage(byte[] byteArrayImg)
        {
            MemoryStream msImage = new MemoryStream(byteArrayImg);
            Image theImage = Image.FromStream(msImage);
            msImage.Dispose();
            return theImage;
        }
        
        public void AddImage(UdpClient thisComputer, IPEndPoint client)
        {
            ///<summary>
            ///When a new client is added his image is added
            ///to the ImageList thus appear on the gui.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<returns>Void</returns>
            thisComputer.Receive(ref client);
            Image image = GetAnImage(clientSocket);
            form.ImageList1.Images.Add(image);
            form.ListView1.Items.Add(new ListViewItem(ip, form.ImageList1.Images.Count - 1));
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
            foreach (ListViewItem item in form.ListView1.Items)
            {
                if (item.Text.Equals(ip))
                {
                    form.ImageList1.Images[i] = image;
                    break;
                }
                i++;
            }

        }

    }

    class ForStream
    {
        //This class if for the thread get stream to use.
        UdpClient clientSocket;
        SessionWithServer mainClass;

        public ForStream(UdpClient clientSocket, SessionWithServer mainClass)
        {
            this.clientSocket = clientSocket;
            this.mainClass = mainClass;
        }

        public void GetStream()
        {
            byte[] lenOfImage = new byte[7];
            byte[] encodedImg = new byte[0];


            while (true)
            {
                clientSocket.Receive();
                Image img = mainClass.GetAnImage(clientSocket);
                mainClass.ChangeImage(img, BitConverter.ToString(ipArray));
            }
        }
    }
}
