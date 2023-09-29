
// import AWS from 'aws-sdk';
// let ses = new AWS.SES();

import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";
const ses = new SESClient({ region: "eu-west-1" });

const sendEmail = async (event) => {
    let emailParams = new SendEmailCommand({
        Destination: {
          ToAddresses: JSON.parse(process.env.TO)
        },
        Message: {
          Body: {
            Text: {
              Data: event.report
            }
          },
          Subject: {
            Data: "test subject"
          }
        },
        Source: process.env.FROM
      });
    
    try {
        let res = await ses.send(emailParams);
        return res;
    } catch (err) {
        console.log(err)
    }
}

export const handler = sendEmail