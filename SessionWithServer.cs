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

namespace teacher_gui_windows_forms
{
    class SessionWithServer
    {
        private int port = 1027;
        private string host = "127.0.0.1";
        private List<Socket> clientsSockets = new List<Socket>();
        private TeacherGUI form;
        private Socket mainSocket;


        public SessionWithServer(TeacherGUI form)
        {
            ///<summary>
            ///The structive function.
            ///</summary>
            ///<param name="form">The GUI..</param>
            mainSocket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
            mainSocket.Connect(host, port);
            this.form = form;
        }

        public void AddClient()
        {
            ///<summary>
            ///Connects another socket for another client with the server.
            ///Adds the socket to the clientsSockets.
            ///</summary>
            ///<returns>Void</returns>
            Socket clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            clientSocket.Connect(this.host, this.port);
            Thread.
            this.clientsSockets.Add(clientSocket);
        }

        public void GetStream(Socket clientSocket)
        {
            while (true)
            {
                clientSocket.Receive()
            }
        }
        
        public void AddImage(Image image)
        {
            ///<summary>
            ///When a new client is added his image is added
            ///to the ImageList thus appear on the gui.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<returns>Void</returns>
            this.form.ImageList1.Images.Add(image);
        }

        public void ChangeImage(Image image, String ip)
        {
            ///<summary>
            ///Whenever a new image is received, this function changes the client's image to the current image.
            ///</summary>
            ///<param name="image">An image.</param>
            ///<param name="ip">Am ip of a client.</param>
            ///<returns>Void</returns>
            int i = 0;
            foreach (ListViewItem item in this.form.ListView1.Items)
            {
                if (item.Text.Equals(ip))
                {
                    this.form.ImageList1.Images[i] = image;
                    break;
                }
                i++;
            }
            
        }


    }

    class DealingWithClients
    {
        //This class if for the threads to use.
        private 
    }
}

